# SIEMENS | Fluorospot Compact S1 — header census

2 DICOM headers under `/rs/rs_grp_oschome/go2432/data/spinesac/drive` (samples: datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/SCN 11/1.dcm, datasets-20260219T101916Z-1-001/datasets/BMJH/SKANRAY/SCN 11/1LP.dcm).

## Exposure and geometry (per frame)

| field | n | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| pulse_ms | 2 | 6 | 6.025 | 6.25 | 6.475 | 6.5 |
| sid_mm | 2 | 1011 | 1011 | 1011 | 1011 | 1011 |
| imager_pixel_mm | 2 | 0.209 | 0.209 | 0.209 | 0.209 | 0.209 |

## Public tags

| tag | n | distinct | most common values (count) |
|---|---:|---:|---|
| Manufacturer | 2 | 1 | SIEMENS (2) |
| ManufacturerModelName | 2 | 1 | Fluorospot Compact S1 (2) |
| SoftwareVersions | 2 | 1 | VG21J\VA20H (2) |
| Modality | 2 | 1 | XA (2) |
| ImageType | 2 | 1 | ORIGINAL\PRIMARY\SINGLE PLANE\FLUORO\SINGLE (2) |
| SOPClassUID | 2 | 1 | 1.2.840.10008.5.1.4.1.1.12.1 (2) |
| Rows | 2 | 1 | 1024 (2) |
| Columns | 2 | 1 | 1024 (2) |
| BitsAllocated | 2 | 1 | 16 (2) |
| BitsStored | 2 | 1 | 16 (2) |
| HighBit | 2 | 1 | 15 (2) |
| PixelRepresentation | 2 | 1 | 0 (2) |
| PhotometricInterpretation | 2 | 1 | MONOCHROME2 (2) |
| PixelIntensityRelationship | 2 | 1 | LIN (2) |
| WindowCenter | 2 | 1 | 33600 (2) |
| WindowWidth | 2 | 1 | 56000 (2) |
| ImagerPixelSpacing | 2 | 1 | 0.2090\0.2090 (2) |
| DistanceSourceToDetector | 2 | 1 | 1011 (2) |
| PositionerType | 2 | 1 | CARM (2) |
| AveragePulseWidth | 2 | 2 | 6.5 (1); 6 (1) |
| RadiationSetting | 2 | 1 | SC (2) |
| RadiationMode | 2 | 1 | PULSED (2) |
| FilterType | 2 | 1 | CU_0.1_MM (2) |
| Grid | 2 | 1 | FOCUSED (2) |
| FieldOfViewShape | 2 | 1 | ROUND (2) |
| FieldOfViewDimensions | 2 | 1 | 215 (2) |
| FieldOfViewOrigin | 2 | 1 | 0\0 (2) |
| LossyImageCompression | 2 | 1 | 00 (2) |
| PatientOrientation | 2 | 1 |  (2) |
| ViewPosition | 2 | 1 |  (2) |
| ProtocolName | 2 | 1 | Ortho SPINE Fat (2) |
| PerformedProcedureStepDescription | 2 | 1 | Spine (2) |
| SeriesDescription | 2 | 1 | Ortho SPINE Fat (2) |
| AcquisitionDeviceProcessingCode | 2 | 1 | 0 (2) |
| BurnedInAnnotation | 2 | 1 | NO (2) |
| DerivationDescription | 2 | 2 | <FlipH=NO><FlipV=NO><Rotate=349º> (1); <FlipH=NO><FlipV=NO><Rotate=7º> (1) |
| StationName | 2 | 1 | 532163b1d0 (2) |
| DeviceSerialNumber | 2 | 1 | 9caaa6b8f2 (2) |

Identity tags present (values never copied): {'PatientName': 2, 'PatientID': 2, 'PatientBirthDate': 2, 'InstitutionName': 2, 'ReferringPhysicianName': 2, 'InstitutionAddress': 2, 'PatientSex': 2, 'PatientAge': 2}

## Private tags

Private creators: [('SIEMENS_FLCOMPACT_VA01A_PROC', 138), ('Siemens: Thorax/Multix FD Raw Image Settings', 30), ('Siemens: Thorax/Multix FD Post Processing', 24), ('Siemens: Thorax/Multix FD Lab Settings', 8)]

| tag creator VR | n | distinct | values |
|---|---:|---:|---|
| (0017,0010)  LO | 2 | 1 | SIEMENS_FLCOMPACT_VA01A_PROC (2) |
| (0017,100a) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,100b) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 21 (2) |
| (0017,100c) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 1 (2) |
| (0017,100d) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 10.0 (2) |
| (0017,100e) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 |  (2) |
| (0017,100f) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 | Cu 0.1 mm (2) |
| (0017,1010) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,1011) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,1016) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1017) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 512 (2) |
| (0017,1018) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 384 (2) |
| (0017,101b) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,101c) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,101e) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,101f) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,1020) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,1021) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1022) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1023) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1024) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 40 (2) |
| (0017,1025) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 2500 (2) |
| (0017,1026) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1027) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1028) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 0.0 (2) |
| (0017,1029) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 0.0 (2) |
| (0017,1048) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 1 (2) |
| (0017,1049) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,104d) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,104e) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 | 20250503 (2) |
| (0017,104f) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 2 | 1533590137 (1); 1539090455 (1) |
| (0017,1050) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 2 (2) |
| (0017,1052) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 3 (2) |
| (0017,1053) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 5 (2) |
| (0017,1054) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 30 (2) |
| (0017,1055) SIEMENS_FLCOMPACT_VA01A_PROC SS | 2 | 1 | 0 (2) |
| (0017,105c) SIEMENS_FLCOMPACT_VA01A_PROC OW | 2 | 1 | <10240 bytes> (2) |
| (0017,1064) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 2.5 (2) |
| (0017,1066) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1067) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 512 (2) |
| (0017,1068) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 384 (2) |
| (0017,1085) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1086) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 1 (2) |
| (0017,1087) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1088) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 40 (2) |
| (0017,1089) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 2500 (2) |
| (0017,108a) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,108b) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,108c) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 0.0 (2) |
| (0017,108d) SIEMENS_FLCOMPACT_VA01A_PROC FL | 2 | 1 | 0.0 (2) |
| (0017,108e) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 1024 (2) |
| (0017,108f) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 1024 (2) |
| (0017,1090) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1091) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1092) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,1093) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10a0) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10a1) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10a2) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 | 0.0 (2) |
| (0017,10aa) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 41 (2) |
| (0017,10ab) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10b0) SIEMENS_FLCOMPACT_VA01A_PROC DS | 2 | 1 | 0 (2) |
| (0017,10bf) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 | Ortho SPINE Fat (2) |
| (0017,10c0) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 | Spine (2) |
| (0017,10c1) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 1 (2) |
| (0017,10c2) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10c3) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10c4) SIEMENS_FLCOMPACT_VA01A_PROC LO | 2 | 1 |  (2) |
| (0017,10e0) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 0 (2) |
| (0017,10e1) SIEMENS_FLCOMPACT_VA01A_PROC US | 2 | 1 | 1 (2) |
| (0019,0010)  LO | 2 | 1 | Siemens: Thorax/Multix FD Lab Settings (2) |
| (0019,1006) Siemens: Thorax/Multix FD Lab Settings FD | 2 | 1 | 100.0 (2) |
| (0019,1007) Siemens: Thorax/Multix FD Lab Settings FD | 2 | 1 | 0.0 (2) |
| (0019,1008) Siemens: Thorax/Multix FD Lab Settings US | 2 | 1 | 0 (2) |
| (0019,1009) Siemens: Thorax/Multix FD Lab Settings LO | 2 | 1 | NO (2) |
| (0021,0010)  LO | 2 | 1 | Siemens: Thorax/Multix FD Post Processing (2) |
| (0021,1008) Siemens: Thorax/Multix FD Post Processing US | 2 | 1 | 0 (2) |
| (0021,1009) Siemens: Thorax/Multix FD Post Processing SL | 2 | 1 | 2100 (2) |
| (0021,100a) Siemens: Thorax/Multix FD Post Processing SL | 2 | 1 | 3500 (2) |
| (0021,100b) Siemens: Thorax/Multix FD Post Processing SS | 2 | 1 | 0 (2) |
| (0021,1013) Siemens: Thorax/Multix FD Post Processing SS | 2 | 2 | 349 (1); 7 (1) |
| (0021,1014) Siemens: Thorax/Multix FD Post Processing US | 2 | 1 | 0 (2) |
| (0021,1015) Siemens: Thorax/Multix FD Post Processing SS | 2 | 1 | -50 (2) |
| (0021,1016) Siemens: Thorax/Multix FD Post Processing DS | 2 | 1 | 0.08 (2) |
| (0021,1017) Siemens: Thorax/Multix FD Post Processing LO | 2 | 1 | Cios Connect (2) |
| (0021,1018) Siemens: Thorax/Multix FD Post Processing LO | 2 | 1 | Image intensifier (2) |
| (0021,1030) Siemens: Thorax/Multix FD Post Processing SH | 2 | 1 | 0 (2) |
| (0021,1031) Siemens: Thorax/Multix FD Post Processing SH | 2 | 1 | 1 (2) |
| (0025,0010)  LO | 2 | 1 | Siemens: Thorax/Multix FD Raw Image Settings (2) |
| (0025,1000) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 0 (2) |
| (0025,100c) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 30 (2) |
| (0025,100d) Siemens: Thorax/Multix FD Raw Image Settings FL | 2 | 1 | 0.0 (2) |
| (0025,100e) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 3 (2) |
| (0025,100f) Siemens: Thorax/Multix FD Raw Image Settings FL | 2 | 1 | 2.5 (2) |
| (0025,1010) Siemens: Thorax/Multix FD Raw Image Settings LT | 2 | 2 | 1.3.12.2.1107.5.12.18.21551.1.20250503153123\1_1 (1); 1.3.12.2.1107.5.12.18.21551.1.20250503153808\1_1 (1) |
| (0025,1018) Siemens: Thorax/Multix FD Raw Image Settings US | 2 | 1 | 0 (2) |
| (0025,1019) Siemens: Thorax/Multix FD Raw Image Settings US | 2 | 1 | 0 (2) |
| (0025,1031) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 0 (2) |
| (0025,1032) Siemens: Thorax/Multix FD Raw Image Settings DS | 2 | 1 | 0.00 (2) |
| (0025,1033) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 0 (2) |
| (0025,1034) Siemens: Thorax/Multix FD Raw Image Settings SS | 2 | 1 | 0 (2) |
| (0025,1035) Siemens: Thorax/Multix FD Raw Image Settings LO | 2 | 1 |  (2) |
| (0025,1036) Siemens: Thorax/Multix FD Raw Image Settings DS | 2 | 1 | 0 (2) |
| (0025,1037) Siemens: Thorax/Multix FD Raw Image Settings DS | 2 | 1 | 0 (2) |
