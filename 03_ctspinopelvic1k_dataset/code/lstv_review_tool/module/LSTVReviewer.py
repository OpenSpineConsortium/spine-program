# source-of-copy: the May 2026 NeurIPS workspace (lstv_review/lstv_review/module/LSTVReviewer.py); not a repository; scripts/LSTVReviewer.py of the CTSpinoPelvic1K repository is the tracked twin of LSTVReviewer.py; copied 2026-10-08
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""
LSTVReviewer.py
3D Slicer scripted module for the CTSpinoPelvic1K LSTV annotation
workflow.

================================================================
INSTALLATION (no coding required, ~2 minutes)
================================================================

1. Save this file (LSTVReviewer.py) into a new folder on your
   computer. The folder name and location don't matter, but pick
   somewhere stable. Examples:

       macOS / Linux:  /Users/yourname/lstv-reviewer/LSTVReviewer.py
       Windows:        <laptop drive>/Users\\yourname\\lstv-reviewer\\LSTVReviewer.py

   IMPORTANT: the folder must contain ONLY this file (no other
   .py files), and the filename MUST be exactly LSTVReviewer.py
   (case-sensitive).

2. Open 3D Slicer (version 5.x or newer).
3. From the menu bar:  Edit  ->  Application Settings
4. In the left panel of the Settings window, click "Modules".
5. Scroll down to "Additional module paths".
6. Click the green "Add" button (the + icon).
7. Navigate to and SELECT THE FOLDER (not the .py file itself)
   that contains LSTVReviewer.py. Click "Open" / "Select Folder".
8. Click "OK" at the bottom of the Application Settings window.
9. Slicer will prompt to restart. Click "Yes".
10. After Slicer restarts, look at the "Modules" dropdown in the
    top-left toolbar. Under the "Annotation" category, click
    "LSTV Reviewer".

================================================================
USAGE
================================================================

1. Click "Browse..." and select the lstv_review/ folder.
2. Pick a case from the dropdown.
3. Click "Load Selected Case".  The CT, segmentation masks, and
   landmark template all load automatically. Place mode turns on
   automatically and the first unplaced landmark is pre-selected.
4. Hover over any slice viewer -> cursor becomes a crosshair ->
   click on the anatomical location. The fiducial places and
   Slicer auto-advances to the next landmark.
5. For landmarks that don't apply to this case: right-click the
   fiducial in the Control Points list -> "Unset position".
6. Switch back to LSTV Reviewer module and click "Save Landmarks".
7. Click "Open review.txt" to fill in the brief categorical form.
8. Click "Next incomplete" or pick another case. Repeat.
"""

# ============================================================
# Module declaration
# ============================================================
import logging
import os
from pathlib import Path

import qt
import slicer
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleWidget,
)


SUBTYPE_DIRS = ["lumb", "sacr_count", "semisacralization",
                "sacralization", "ambiguous", "reference_normal"]

# vtkMRMLMarkupsNode position-status enum values
POS_UNDEFINED = 0
POS_PREVIEW = 1
POS_DEFINED = 2
POS_MISSING = 3


# ============================================================
class LSTVReviewer(ScriptedLoadableModule):
    """Module entry point registered with Slicer."""

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        parent.title = "LSTV Reviewer"
        parent.categories = ["Annotation"]
        parent.dependencies = []
        parent.contributors = ["Gregory Schwing (Wayne State University)"]
        parent.helpText = (
            "LSTV Reviewer streamlines per-case landmark annotation for "
            "the CTSpinoPelvic1K LSTV review package. Browse to the "
            "lstv_review/ folder, pick a case, click Load. CT, masks, "
            "and landmark template load automatically. Place fiducials, "
            "click Save."
        )
        parent.acknowledgementText = (
            "Part of CTSpinoPelvic1K, a CT-native LSTV-stratified "
            "spine-pelvis segmentation benchmark targeting 3D Slicer "
            "deployment as a TotalSegmentator replacement for "
            "spinal CT."
        )


# ============================================================
class LSTVReviewerWidget(ScriptedLoadableModuleWidget):
    """The panel that appears in the Modules area."""

    # ---------- setup ----------
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # State
        self.review_root = None        # Path to lstv_review/
        self.cases = []                # list of dicts: subtype, token, dir, complete
        self.current_case = None       # currently-loaded case dict
        self.current_markup_node = None
        self._observer_tags = []       # observer cleanup tracking

        # ---------- 1. Folder ----------
        groupFolder = qt.QGroupBox("1. Review folder")
        layoutFolder = qt.QHBoxLayout(groupFolder)
        self.folderLabel = qt.QLabel("(not set)")
        self.folderLabel.setStyleSheet("color: gray; font-style: italic;")
        self.folderLabel.setWordWrap(True)
        self.btnBrowse = qt.QPushButton("Browse...")
        self.btnBrowse.connect("clicked()", self.onBrowse)
        layoutFolder.addWidget(self.folderLabel, 1)
        layoutFolder.addWidget(self.btnBrowse)
        self.layout.addWidget(groupFolder)

        # ---------- 2. Cases ----------
        groupCase = qt.QGroupBox("2. Cases")
        layoutCase = qt.QVBoxLayout(groupCase)
        self.lblProgress = qt.QLabel("0 / 0 complete")
        self.lblProgress.setStyleSheet("font-weight: bold;")
        self.cmbCase = qt.QComboBox()
        self.cmbCase.setEnabled(False)
        rowCaseBtns = qt.QHBoxLayout()
        self.btnRefresh = qt.QPushButton("Refresh")
        self.btnRefresh.connect("clicked()", self.refreshCases)
        self.btnRefresh.setEnabled(False)
        self.btnNextIncomplete = qt.QPushButton("Next incomplete")
        self.btnNextIncomplete.connect("clicked()", self.onNextIncomplete)
        self.btnNextIncomplete.setEnabled(False)
        rowCaseBtns.addWidget(self.btnRefresh)
        rowCaseBtns.addWidget(self.btnNextIncomplete)
        layoutCase.addWidget(self.lblProgress)
        layoutCase.addWidget(self.cmbCase)
        layoutCase.addLayout(rowCaseBtns)
        self.layout.addWidget(groupCase)

        # ---------- 3. Annotate ----------
        groupAct = qt.QGroupBox("3. Annotate")
        layoutAct = qt.QVBoxLayout(groupAct)
        self.btnLoad = qt.QPushButton("Load Selected Case")
        self.btnLoad.setStyleSheet(
            "QPushButton { font-weight: bold; padding: 10px; "
            "background-color: #2a6496; color: white; border-radius: 4px; }"
            "QPushButton:disabled { background-color: #888; }"
        )
        self.btnLoad.connect("clicked()", self.onLoadCase)
        self.btnLoad.setEnabled(False)

        self.btnSave = qt.QPushButton("Save Landmarks")
        self.btnSave.setStyleSheet(
            "QPushButton { font-weight: bold; padding: 10px; "
            "background-color: #4a8a4a; color: white; border-radius: 4px; }"
            "QPushButton:disabled { background-color: #888; }"
        )
        self.btnSave.connect("clicked()", self.onSaveLandmarks)
        self.btnSave.setEnabled(False)

        self.btnReview = qt.QPushButton("Open review.txt")
        self.btnReview.connect("clicked()", self.onOpenReview)
        self.btnReview.setEnabled(False)

        layoutAct.addWidget(self.btnLoad)
        layoutAct.addWidget(self.btnSave)
        layoutAct.addWidget(self.btnReview)
        self.layout.addWidget(groupAct)

        # ---------- Status ----------
        groupStatus = qt.QGroupBox("Status")
        layoutStatus = qt.QVBoxLayout(groupStatus)
        self.lblStatus = qt.QLabel("Select a review folder to begin.")
        self.lblStatus.setWordWrap(True)
        self.lblStatus.setTextFormat(qt.Qt.RichText)
        layoutStatus.addWidget(self.lblStatus)
        self.layout.addWidget(groupStatus)

        # ---------- Help ----------
        helpText = qt.QLabel(
            "<b>Workflow:</b><br>"
            "<small>"
            "1. Browse to your <i>lstv_review/</i> folder.<br>"
            "2. Pick a case (\u2610 pending, \u2713 saved).<br>"
            "3. Click <b>Load Selected Case</b>.<br>"
            "4. Hover over a slice viewer \u2192 cursor becomes "
            "crosshair \u2192 click anatomical location.<br>"
            "5. Right-click a landmark in Control Points list "
            "\u2192 <i>Unset position</i> if absent.<br>"
            "6. Click <b>Save Landmarks</b>.<br>"
            "7. Click <b>Open review.txt</b>, complete, save.<br>"
            "8. Click <b>Next incomplete</b>.<br>"
            "</small>"
        )
        helpText.setWordWrap(True)
        helpText.setTextFormat(qt.Qt.RichText)
        helpText.setStyleSheet(
            "padding: 8px; background-color: #f0f0f0; "
            "border-radius: 4px; color: #333;")
        self.layout.addWidget(helpText)

        self.layout.addStretch()

    # ---------- 1. Folder selection ----------
    def onBrowse(self):
        start = (str(self.review_root.parent)
                 if self.review_root else os.path.expanduser("~"))
        path = qt.QFileDialog.getExistingDirectory(
            None, "Select lstv_review folder", start)
        if not path:
            return
        path = Path(path)
        if not any((path / sd).is_dir() for sd in SUBTYPE_DIRS):
            slicer.util.warningDisplay(
                "Selected folder does not contain expected LSTV "
                "subtype subdirectories.\n\n"
                "Expected at least one of: "
                + ", ".join(SUBTYPE_DIRS)
                + "\n\nPlease select the lstv_review/ root folder.")
            return
        self.review_root = path
        self.folderLabel.setText(str(path))
        self.folderLabel.setStyleSheet("color: black;")
        self.refreshCases()
        self.cmbCase.setEnabled(True)
        self.btnRefresh.setEnabled(True)
        self.btnNextIncomplete.setEnabled(True)
        self.btnLoad.setEnabled(True)

    # ---------- 2. Case list ----------
    def refreshCases(self):
        if self.review_root is None:
            return
        prev_dir = self.current_case["dir"] if self.current_case else None
        self.cases = []
        for sd in SUBTYPE_DIRS:
            sub = self.review_root / sd
            if not sub.is_dir():
                continue
            for d in sorted(sub.iterdir()):
                if not (d.is_dir() and d.name.startswith("token_")):
                    continue
                self.cases.append({
                    "subtype": sd,
                    "token": d.name.replace("token_", ""),
                    "dir": d,
                    "complete": (d / "landmarks.mrk.json").exists(),
                })
        n_complete = sum(1 for c in self.cases if c["complete"])
        self.lblProgress.setText(
            f"{n_complete} / {len(self.cases)} complete")
        self.cmbCase.clear()
        for c in self.cases:
            mark = "\u2713" if c["complete"] else "\u2610"
            self.cmbCase.addItem(
                f"  {mark}  {c['subtype']} / token_{c['token']}")
        if prev_dir is not None:
            for i, c in enumerate(self.cases):
                if c["dir"] == prev_dir:
                    self.cmbCase.setCurrentIndex(i)
                    break

    def selectedCase(self):
        idx = self.cmbCase.currentIndex
        if idx < 0 or idx >= len(self.cases):
            return None
        return self.cases[idx]

    def onNextIncomplete(self):
        if not self.cases:
            return
        idx = self.cmbCase.currentIndex
        for offset in range(1, len(self.cases) + 1):
            j = (idx + offset) % len(self.cases)
            if not self.cases[j]["complete"]:
                self.cmbCase.setCurrentIndex(j)
                return
        slicer.util.infoDisplay("All cases are complete!")

    # ---------- 3a. Load case ----------
    def onLoadCase(self):
        case = self.selectedCase()
        if case is None:
            return

        # Warn if there's potentially-unsaved work
        if (self.current_case is not None
                and self.current_markup_node is not None):
            n_placed = self._countPlaced(self.current_markup_node)
            saved_path = self.current_case["dir"] / "landmarks.mrk.json"
            if n_placed > 0 and not saved_path.exists():
                if not slicer.util.confirmYesNoDisplay(
                        f"You have {n_placed} placed landmarks in the "
                        f"current case ({self.current_case['subtype']} / "
                        f"token_{self.current_case['token']}) that have "
                        f"not been saved.\n\nDiscard them and load the "
                        f"new case?"):
                    return

        # Clean up prior observers
        self._cleanupObservers()

        self.current_case = case
        self.current_markup_node = None
        slicer.mrmlScene.Clear(0)

        # CT
        ct_files = sorted(case["dir"].glob("ct*.nii.gz"))
        if not ct_files:
            slicer.util.warningDisplay(f"No CT files in {case['dir']}")
            return
        for f in ct_files:
            try:
                slicer.util.loadVolume(str(f))
            except Exception as e:
                logging.warning(f"Failed to load {f}: {e}")

        # Labels as segmentations
        label_files = sorted(case["dir"].glob("label*.nii.gz"))
        if not label_files:
            legacy = [case["dir"] / n for n in
                      ("spine_mask.nii.gz", "pelvic_mask.nii.gz")]
            label_files = [p for p in legacy if p.exists()]
        for p in label_files:
            try:
                slicer.util.loadSegmentation(str(p))
            except Exception as e:
                logging.warning(f"Failed to load {p}: {e}")

        # Landmarks
        existing = case["dir"] / "landmarks.mrk.json"
        template = case["dir"] / "landmarks_template.mrk.json"
        landmark_path = existing if existing.exists() else template
        if not landmark_path.exists():
            slicer.util.warningDisplay(
                f"No landmark template in {case['dir']}")
            return
        try:
            self.current_markup_node = slicer.util.loadMarkups(
                str(landmark_path))
        except Exception as e:
            slicer.util.warningDisplay(
                f"Failed to load landmark template: {e}")
            return

        node = self.current_markup_node

        # Hide all unplaced (preview) points so they don't stack at origin
        for i in range(node.GetNumberOfControlPoints()):
            placed = node.GetNthControlPointPositionStatus(i) == POS_DEFINED
            node.SetNthControlPointVisibility(i, placed)

        # Observer: auto-show points as user places them, auto-advance
        def on_point_modified(caller, event):
            try:
                for i in range(caller.GetNumberOfControlPoints()):
                    placed = (caller.GetNthControlPointPositionStatus(i)
                              == POS_DEFINED)
                    caller.SetNthControlPointVisibility(i, placed)
                # Update status
                n_placed = self._countPlaced(caller)
                n_total = caller.GetNumberOfControlPoints()
                if self.current_case is not None:
                    self.lblStatus.setText(
                        f"<b>Loaded:</b> {self.current_case['subtype']} / "
                        f"token_{self.current_case['token']}<br>"
                        f"<b>Landmarks:</b> {n_placed} / {n_total} placed"
                        f"<br><b>Place mode is ON.</b> Hover over a slice "
                        f"viewer \u2192 crosshair \u2192 click.")
            except Exception as e:
                logging.warning(f"Observer callback failed: {e}")

        try:
            tag1 = node.AddObserver(
                slicer.vtkMRMLMarkupsNode.PointModifiedEvent,
                on_point_modified)
            tag2 = node.AddObserver(
                slicer.vtkMRMLMarkupsNode.PointPositionDefinedEvent,
                on_point_modified)
            self._observer_tags.append((node, tag1))
            self._observer_tags.append((node, tag2))
        except Exception as e:
            logging.warning(f"Failed to attach observer: {e}")

        # Find first unplaced point
        first_unplaced = -1
        for i in range(node.GetNumberOfControlPoints()):
            if node.GetNthControlPointPositionStatus(i) != POS_DEFINED:
                first_unplaced = i
                break

        # Fit slice viewers
        slicer.app.applicationLogic().FitSliceToAll()

        # Switch to Markups module
        slicer.util.selectModule("Markups")

        # Activate Place mode (deferred so module finishes switching)
        def activate_placement():
            try:
                selectionNode = (slicer.app.applicationLogic()
                                 .GetSelectionNode())
                selectionNode.SetReferenceActivePlaceNodeClassName(
                    "vtkMRMLMarkupsFiducialNode")
                selectionNode.SetActivePlaceNodeID(node.GetID())
                interactionNode = (slicer.app.applicationLogic()
                                   .GetInteractionNode())
                interactionNode.SetPlaceModePersistence(1)
                interactionNode.SetCurrentInteractionMode(
                    interactionNode.Place)
                if first_unplaced >= 0:
                    try:
                        node.GetDisplayNode().SetActiveControlPoint(
                            first_unplaced)
                    except Exception:
                        pass
            except Exception as e:
                logging.warning(f"Place-mode activation failed: {e}")

        qt.QTimer.singleShot(300, activate_placement)

        # Status
        n_placed = self._countPlaced(node)
        n_total = node.GetNumberOfControlPoints()
        loaded_existing = existing.exists()
        source_note = ("loaded from previous save"
                       if loaded_existing else "fresh template")
        self.lblStatus.setText(
            f"<b>Loaded:</b> {case['subtype']} / "
            f"token_{case['token']}<br>"
            f"<b>Landmarks:</b> {n_placed} / {n_total} placed "
            f"({source_note})<br>"
            f"<b>Place mode activating...</b> Hover over a slice "
            f"viewer \u2192 cursor becomes crosshair \u2192 click on "
            f"the anatomical location.")
        self.btnSave.setEnabled(True)
        self.btnReview.setEnabled(True)

    def _cleanupObservers(self):
        for node, tag in self._observer_tags:
            try:
                if node is not None:
                    node.RemoveObserver(tag)
            except Exception:
                pass
        self._observer_tags = []

    def _countPlaced(self, node):
        if node is None:
            return 0
        try:
            n = node.GetNumberOfControlPoints()
        except Exception:
            return 0
        count = 0
        for i in range(n):
            try:
                if node.GetNthControlPointPositionStatus(i) == POS_DEFINED:
                    count += 1
            except Exception:
                continue
        return count

    # ---------- 3b. Save landmarks ----------
    def onSaveLandmarks(self):
        if self.current_case is None or self.current_markup_node is None:
            slicer.util.warningDisplay("No case is loaded.")
            return
        out_path = self.current_case["dir"] / "landmarks.mrk.json"
        try:
            storage = self.current_markup_node.GetStorageNode()
            if storage is None:
                self.current_markup_node.CreateDefaultStorageNode()
                storage = self.current_markup_node.GetStorageNode()
            storage.SetFileName(str(out_path))
            ok = storage.WriteData(self.current_markup_node)
        except Exception as e:
            slicer.util.warningDisplay(f"Save failed: {e}")
            return
        if not ok:
            slicer.util.warningDisplay(
                f"Storage node returned failure for {out_path}")
            return
        n_placed = self._countPlaced(self.current_markup_node)
        n_total = self.current_markup_node.GetNumberOfControlPoints()
        slicer.util.delayDisplay(
            f"Saved landmarks.mrk.json\n"
            f"({n_placed} / {n_total} placed)", 2000)
        self.refreshCases()
        self.lblStatus.setText(
            f"<b>Saved:</b> {self.current_case['subtype']} / "
            f"token_{self.current_case['token']}<br>"
            f"<b>Landmarks:</b> {n_placed} / {n_total} placed")

    # ---------- 3c. Open review.txt ----------
    def onOpenReview(self):
        if self.current_case is None:
            slicer.util.warningDisplay("No case is loaded.")
            return
        review = self.current_case["dir"] / "review.txt"
        if not review.exists():
            slicer.util.warningDisplay(
                f"review.txt not found in {self.current_case['dir']}")
            return
        url = qt.QUrl.fromLocalFile(str(review))
        if not qt.QDesktopServices.openUrl(url):
            slicer.util.warningDisplay(
                f"Could not open {review} with the default text "
                f"editor. Please open the file manually.")


# ============================================================
class LSTVReviewerLogic(ScriptedLoadableModuleLogic):
    """Stub; UI logic is in the Widget."""
    pass
