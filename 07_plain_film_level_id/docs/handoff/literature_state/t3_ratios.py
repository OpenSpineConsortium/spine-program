"""Topic 3: programme n divided by published-study n, per task. Every input is copied from a file named in the note."""

rows = [
    # (task, comparison label, programme n, study n)
    ("radiograph", "level-bank films 9,108 vs VertXNet images 512+226+445", 9108, 512 + 226 + 445),
    ("radiograph", "level-bank films 9,108 vs Kim 2024 radiographs 150", 9108, 150),
    ("radiograph", "level-bank films 9,108 vs BUU-LSPINE release films 7,200", 9108, 7200),
    ("radiograph", "held-out vertebrae CSXA 3,720 + BUU 2,698 vs Kim 2024 radiographs 150 (units differ)", 3720 + 2698, 150),
    ("carm", "naming frames 296 vs VDVM C-arm test images 31", 296, 31),
    ("carm", "lateral vertebrae scored 617 vs VDVM C-arm test images 31 (units differ)", 617, 31),
    ("carm", "mobile C-arm real frames 778 vs VDVM C-arm images 382+31", 778, 382 + 31),
    ("carm", "mobile C-arm real frames 778 vs Rao 2024 images 578", 778, 578),
    ("carm", "held-out detector test frames 56 vs Rao 2024 test images 20", 56, 20),
    ("carm", "devices with real frames and 3-D truth 5 vs Rao 2024 C-arms 3", 5, 3),
    ("carm", "mobile C-arms with real frames 3 vs Rao 2024 C-arms 3", 3, 3),
    ("carm", "naming cases 148 vs Huang 2022 cadavers 13", 148, 13),
    ("carm", "naming frames 296 vs Huang 2022 test images 100", 296, 100),
    ("carm", "TotalSegmentator scans rendered 1,935 vs Huang 2022 training CTs 297", 1935, 297),
    ("carm", "naming cases 148 vs Desai 2026 cases 75", 148, 75),
    ("carm", "naming frames 296 vs De Silva 2016 radiographs 398", 296, 398),
    ("carm", "naming cases 148 vs De Silva 2016 preoperative CTs 178", 148, 178),
    ("carm", "naming frames 296 vs Manbachi 2018 images 62", 296, 62),
    ("carm", "real frames with 3-D truth 4,276 vs Zheng 2018 real X-rays 420", 4276, 420),
    ("lstv2d", "real 2-D transitional positives 144 BUU + 3 C-ArmLSpine vs Kwak 2025 LSTV films 1,941", 144 + 3, 1941),
    ("lstv2d", "anomalous BUU films in the v6 interior test 128 vs Kwak 2025 LSTV test films 195", 128, 195),
    ("lstv2d", "BUU anomalous studies 144 vs Hanhivaara 2024 LSTV patients 100", 144, 100),
    ("ct", "CTSpinoPelvic1K patients 802 vs VerSe patients 355", 802, 355),
    ("ct", "CTSpinoPelvic1K patients 802 vs VERIDAH CT scans 1,536", 802, 1536),
    ("ct", "CTSpinoPelvic1K patients 802 vs Hanaoka 2017 CTs 300", 802, 300),
    ("ct", "CTSpinoPelvic1K patients 802 vs Schinz 2026 CTs 1,242", 802, 1242),
    ("ct", "CTSpinoPelvic1K patients 802 vs HealthOST CTs 150", 802, 150),
    ("ct", "CTSpinoPelvic1K patients 802 vs TotalSegmentator CTs 1,204", 802, 1204),
    ("ct", "CTSpinoPelvic1K patients 802 vs CTSpine1K volumes 1,005", 802, 1005),
    ("ct", "CTSpinoPelvic1K patients 802 vs Netherton 2020 training scans 803", 802, 803),
    ("ct", "transitional persons with L6 110 vs VerSe'20 L6 cases 47", 110, 47),
    ("ct", "count-changing transitional persons 110+7+12 vs VERIDAH LEA+TEA scans (inferred 0.073*1536 + 0.055*1536)", 110 + 7 + 12, 0.073 * 1536 + 0.055 * 1536),
    ("ct", "transitional persons any subtype 194 vs Hanaoka 2017 transitional subjects 73", 194, 73),
    ("prev", "CT spines with both junction flags 1,113 vs Hanhivaara 2020 CTs 3,855", 1113, 3855),
    ("prev", "CT spines with both junction flags 1,113 vs Doo 2020 whole-spine CTs 1,340", 1113, 1340),
    ("prev", "CT spines with both junction flags 1,113 vs Paik 2013 MRI patients 8,280", 1113, 8280),
    ("prev", "CT spines with both junction flags 1,113 vs Sabri 2025 radiographs 3,147", 1113, 3147),
    ("prev", "CT spines with both junction flags 1,113 vs Nagata 2025 CTs 551", 1113, 551),
    ("prev", "tier-1 acquisition CTs 15,233 (expected, not screened) vs Paik 2013 8,280", 15233, 8280),
]

print("VERIDAH inferred LEA scans:", round(0.073 * 1536, 1), "TEA scans:", round(0.055 * 1536, 1))
for task, label, a, b in rows:
    print(f"{task:8s} | {label} | {a} / {b:.1f} = {a / b:.2f}")
