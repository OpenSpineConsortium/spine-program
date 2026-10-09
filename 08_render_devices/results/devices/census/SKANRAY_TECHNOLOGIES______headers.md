# SKANRAY TECHNOLOGIES | ? — header census

53 DICOM headers under `/rs/rs_grp_oschome/go2432/data/spinesac/drive` (samples: datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/1.2.826.0.1.3680043.9.3558.1107.1326884065.1141120242106200001.DCM, datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/1.2.826.0.1.3680043.9.3558.1107.1326884065.1141120242106200142.DCM, datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/1.2.826.0.1.3680043.9.3558.1107.1326884065.1141120242106200152.DCM, datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/1.2.826.0.1.3680043.9.3558.1107.1326884065.1141120242106200156.DCM, datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/1.2.826.0.1.3680043.9.3558.1107.1326884065.1141120242106200157.DCM).

## Exposure and geometry (per frame)

| field | n | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| kvp | 53 | 41.03 | 42.05 | 46.03 | 52.89 | 70.58 |
| ma | 53 | 590 | 690 | 1090 | 1466 | 3300 |
| ms | 53 | 364 | 455 | 697 | 697 | 727 |
| mas | 53 | 324 | 423.5 | 690 | 968.8 | 1502 |
| primary_deg | 53 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| secondary_deg | 53 | 0.21 | 0.21 | 0.21 | 0.21 | 0.21 |
| entrance_dose_mgy | 53 | 0.03 | 0.036 | 0.05 | 0.12 | 0.38 |
| pixel_mm | 53 | 0.22 | 0.22 | 0.22 | 0.22 | 0.22 |
| imager_pixel_mm | 53 | 0.22 | 0.22 | 0.22 | 0.22 | 0.22 |
| frame_time_ms | 53 | 1000 | 1000 | 1000 | 1000 | 1000 |

## Public tags

| tag | n | distinct | most common values (count) |
|---|---:|---:|---|
| Manufacturer | 53 | 1 | SKANRAY TECHNOLOGIES (53) |
| SoftwareVersions | 53 | 1 | Version 1.15 (53) |
| Modality | 53 | 1 | RF (53) |
| ImageType | 53 | 1 | DERIVED (53) |
| SOPClassUID | 53 | 1 | 1.2.840.10008.5.1.4.1.1.12.1 (53) |
| Rows | 53 | 1 | 1024 (53) |
| Columns | 53 | 1 | 1024 (53) |
| BitsAllocated | 53 | 1 | 16 (53) |
| BitsStored | 53 | 1 | 16 (53) |
| HighBit | 53 | 1 | 15 (53) |
| PixelRepresentation | 53 | 1 | 0 (53) |
| PhotometricInterpretation | 53 | 1 | MONOCHROME2 (53) |
| PixelIntensityRelationship | 53 | 1 | LIN (53) |
| RescaleSlope | 53 | 1 | 0 (53) |
| RescaleIntercept | 53 | 1 | 0 (53) |
| RescaleType | 53 | 1 | 0 (53) |
| WindowCenter | 53 | 50 | 8500 (2); 9950 (2); 10132 (2); 10102 (1); 10214 (1) |
| WindowWidth | 53 | 50 | 15000 (2); 10867 (2); 11534 (2); 11595 (1); 11347 (1) |
| ImagerPixelSpacing | 53 | 1 | 0.22\0.22 (53) |
| PixelSpacing | 53 | 1 | 0.22\0.22 (53) |
| PositionerType | 53 | 1 | NONE (53) |
| PositionerPrimaryAngle | 53 | 1 | 0.01 (53) |
| PositionerSecondaryAngle | 53 | 1 | 0.21 (53) |
| KVP | 53 | 45 | 52.16 (3); 70.58 (2); 47.67 (2); 43.9 (2); 51.93 (2) |
| XRayTubeCurrent | 53 | 12 | 1390 (11); 890 (11); 990 (8); 1290 (4); 1090 (4) |
| ExposureTime | 53 | 11 | 697 (34); 667 (3); 636 (3); 455 (2); 727 (2) |
| RadiationSetting | 53 | 1 | SC (53) |
| ShutterShape | 53 | 1 | RECTANGULAR (53) |
| ShutterLeftVerticalEdge | 53 | 1 | 0 (53) |
| ShutterRightVerticalEdge | 53 | 1 | 1024 (53) |
| ShutterUpperHorizontalEdge | 53 | 1 | 0 (53) |
| ShutterLowerHorizontalEdge | 53 | 1 | 1024 (53) |
| DetectorType | 53 | 1 | DIRECT (53) |
| EntranceDoseInmGy | 53 | 9 | 0.04 (18); 0.07 (11); 0.05 (7); 0.06 (5); 0.03 (3) |
| NumberOfFrames | 53 | 1 | 1 (53) |
| FrameTime | 53 | 1 | 1000 (53) |
| CineRate | 53 | 1 | 1 (53) |
| FrameIncrementPointer | 53 | 1 | (3531,3737)\(3530,0039) (53) |
| LossyImageCompression | 53 | 1 | 00 (53) |
| PatientOrientation | 53 | 1 | L\F (53) |
| PerformedProcedureStepDescription | 53 | 1 | X-RAYS (53) |
| SeriesDescription | 53 | 1 | SNAPSHOT (53) |

Identity tags present (values never copied): {'PatientName': 53, 'PatientID': 53, 'PatientBirthDate': 53, 'InstitutionName': 53, 'ReferringPhysicianName': 53, 'PatientSex': 53}

## Private tags

Private creators: []

| tag creator VR | n | distinct | values |
|---|---:|---:|---|
