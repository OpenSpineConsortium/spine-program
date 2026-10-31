"""The full list for the fixed readings: one study a person of gold tier 3 (the covariates join's
persons) and every gold tier 4 CT the profile job linked, each with its CT where one is on the grid."""
import csv, json, os, sys
M = "/rs/rs_grp_oschome/go2432/morphometry"
D = "/rs/rs_grp_oschome/go2432/data"
TS = D + "/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300"
G4 = "/rs/rs_grp_oschome/go2432/gold4-totalseg"
out = open(sys.argv[1], "w")
for r in csv.DictReader(open(M + "/covariates/40902924/persons.csv")):
    s = r["study"]
    if r["member"] in ("autopet", "enhance_pet"):
        out.write("%s/enhance/masks/%s.nii.gz\tenhance\tenhance\t%s/aws_enhance_pet_ct/raw/%s.nii.gz\n" % (M, s, D, s))
    elif r["member"] == "verse":
        out.write("%s/verse/masks/%s.nii.gz\tverse\tverse\t\n" % (M, s))
    elif r["member"] == "totalseg":
        out.write("%s/verse/totalseg/masks/%s.nii.gz\tverse\ttotalseg\t%s/%s/ct.nii.gz\n" % (M, s, TS, s))
links = "/rs/rs_grp_oschome/go2432/cns-profile/40906591/masks"
cts = {}
for line in open(G4 + "/records.jsonl"):
    rec = json.loads(line)
    cts[rec["id"]] = rec.get("ct", "")
for name in sorted(os.listdir(links)):
    sid = name.split(".")[0]
    out.write("%s/%s\tverse\tgold4\t%s\n" % (links, name, cts.get(sid, "")))
