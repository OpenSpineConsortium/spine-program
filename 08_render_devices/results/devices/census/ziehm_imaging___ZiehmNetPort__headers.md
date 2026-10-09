# ziehm imaging | ZiehmNetPort — header census

8 DICOM headers under `/rs/rs_grp_oschome/go2432/data/spinesac/drive` (samples: datasets-20260219T101916Z-1-001/datasets/BMJH/ZIEHM/SCN 1/AP.dcm, datasets-20260219T101916Z-1-001/datasets/BMJH/ZIEHM/SCN 1/LP.dcm, datasets-20260219T101916Z-1-001/datasets/BMJH/ZIEHM/SCN 10/AP.dcm, datasets-20260219T101916Z-1-001/datasets/BMJH/ZIEHM/SCN 10/LP.dcm, datasets-20260219T101916Z-1-001/datasets/BMJH/ZIEHM/SCN 12/AP.dcm).

## Exposure and geometry (per frame)

| field | n | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| kvp | 8 | 45 | 46.05 | 51.5 | 54.65 | 55 |
| ma | 8 | 2 | 2 | 3.5 | 4 | 4 |
| sid_mm | 8 | 970 | 970 | 970 | 970 | 970 |

## Public tags

| tag | n | distinct | most common values (count) |
|---|---:|---:|---|
| Manufacturer | 8 | 1 | ziehm imaging (8) |
| ManufacturerModelName | 8 | 1 | ZiehmNetPort (8) |
| SoftwareVersions | 8 | 1 | 2.14 (8) |
| Modality | 8 | 1 | XA (8) |
| ImageType | 8 | 1 | ORIGINAL\PRIMARY\SINGLE PLANE (8) |
| SOPClassUID | 8 | 1 | 1.2.840.10008.5.1.4.1.1.12.1 (8) |
| Rows | 8 | 1 | 1024 (8) |
| Columns | 8 | 1 | 1024 (8) |
| BitsAllocated | 8 | 1 | 8 (8) |
| BitsStored | 8 | 1 | 8 (8) |
| HighBit | 8 | 1 | 7 (8) |
| PixelRepresentation | 8 | 1 | 0 (8) |
| PhotometricInterpretation | 8 | 1 | MONOCHROME2 (8) |
| PixelIntensityRelationship | 8 | 1 | LIN (8) |
| WindowCenter | 8 | 1 | 128 (8) |
| WindowWidth | 8 | 1 | 256 (8) |
| DistanceSourceToDetector | 8 | 1 | 970 (8) |
| KVP | 8 | 6 | 54 (2); 50 (2); 53 (1); 48 (1); 55 (1) |
| XRayTubeCurrent | 8 | 3 | 4 (4); 3 (2); 2 (2) |
| XRayTubeCurrentInuA | 8 | 6 | 3800 (2); 2800 (2); 3500 (1); 2300 (1); 4100 (1) |
| RadiationSetting | 8 | 1 | SC (8) |
| RadiationMode | 8 | 1 | CONTINUOUS (8) |
| FocalSpots | 8 | 1 | 0.6 (8) |
| Grid | 8 | 1 | IN (8) |
| CollimatorShape | 8 | 1 | CIRCULAR (8) |
| CenterOfCircularCollimator | 8 | 1 | 287\287 (8) |
| RadiusOfCircularCollimator | 8 | 1 | 288 (8) |
| FieldOfViewShape | 8 | 1 | ROUND (8) |
| PatientOrientation | 8 | 1 | R\F (8) |
| ProtocolName | 8 | 1 |  (8) |
| StationName | 8 | 1 | 0c0aea3542 (8) |
| DeviceSerialNumber | 8 | 1 | e78ef438a7 (8) |

Identity tags present (values never copied): {'PatientName': 8, 'PatientID': 8, 'PatientBirthDate': 8, 'InstitutionName': 8, 'ReferringPhysicianName': 8, 'PerformingPhysicianName': 8, 'PatientSex': 8}

## Private tags

Private creators: []

| tag creator VR | n | distinct | values |
|---|---:|---:|---|
