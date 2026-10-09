# surgio_b51 — header census

901 DICOM headers under `/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked` (samples: C-ArmLSpine/case1/C-arm/0001.dcm, C-ArmLSpine/case1/C-arm/0002.dcm, C-ArmLSpine/case10/C-arm/0001.dcm, C-ArmLSpine/case10/C-arm/0002.dcm, C-ArmLSpine/case100/C-arm/0001.dcm).

## Exposure and geometry (per frame)

| field | n | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| kvp | 901 | 73 | 73 | 111 | 111 | 111 |
| ma | 901 | 12 | 12 | 13 | 26 | 29 |
| ms | 901 | 10 | 10 | 10 | 10 | 10 |
| mas | 901 | 0.12 | 0.12 | 0.13 | 0.26 | 0.29 |
| pulse_ms | 901 | 14 | 15 | 20 | 89 | 163 |
| sid_mm | 901 | 1140 | 1140 | 1140 | 1140 | 1140 |
| sod_mm | 901 | 745 | 745 | 745 | 745 | 745 |
| primary_deg | 901 | -58.1 | -38.8 | 37.4 | 113.6 | 122 |
| secondary_deg | 901 | -0.6 | 0 | 0.6 | 0.9 | 0.9 |
| pixel_mm | 901 | 1 | 1 | 1 | 1 | 1 |

## Public tags

| tag | n | distinct | most common values (count) |
|---|---:|---:|---|
| Manufacturer | 901 | 1 | 一影医疗 (901) |
| ManufacturerModelName | 901 | 1 | Surgio-B51 (901) |
| SoftwareVersions | 901 | 2 | OR01-00.012.001 (683); OR01-00.012.002 (218) |
| Modality | 901 | 1 | XA (901) |
| ImageType | 901 | 1 | ORIGINAL\PRIMARY\SINGLE PLANE (901) |
| SOPClassUID | 901 | 1 | 1.2.840.10008.5.1.4.1.1.12.1 (901) |
| Rows | 901 | 2 | 1024 (602); 2048 (299) |
| Columns | 901 | 2 | 1024 (602); 2048 (299) |
| BitsAllocated | 901 | 1 | 16 (901) |
| BitsStored | 901 | 1 | 16 (901) |
| HighBit | 901 | 1 | 15 (901) |
| PixelRepresentation | 901 | 1 | 0 (901) |
| PhotometricInterpretation | 901 | 1 | MONOCHROME2 (901) |
| PixelIntensityRelationship | 901 | 1 |  (901) |
| RescaleSlope | 901 | 1 | 1 (901) |
| RescaleIntercept | 901 | 1 | 0 (901) |
| WindowCenter | 901 | 786 | 1025 (6); 33811 (4); 1009 (4); 1085 (4); 1086 (4) |
| WindowWidth | 901 | 792 | 73054 (4); 1375 (4); 1325 (4); 1320 (4); 73063 (3) |
| PixelSpacing | 901 | 1 | 1.0000\1.0000 (901) |
| DistanceSourceToDetector | 901 | 1 | 1140 (901) |
| DistanceSourceToPatient | 901 | 1 | 745 (901) |
| PositionerPrimaryAngle | 901 | 123 | 90.0 (138); 0.0 (130); 0.1 (16); 89.9 (11); 122.0 (8) |
| PositionerSecondaryAngle | 901 | 8 | 0.9 (312); 0.6 (280); 0.0 (131); 0.1 (83); 0.7 (46) |
| PositionerPrimaryAngleIncrement | 901 | 1 | 0 (901) |
| PositionerSecondaryAngleIncrement | 901 | 1 | 0 (901) |
| KVP | 901 | 28 | 111 (602); 73 (60); 89 (35); 75 (23); 85 (18) |
| XRayTubeCurrent | 901 | 9 | 12 (301); 13 (301); 26 (118); 25 (109); 24 (48) |
| XRayTubeCurrentInuA | 901 | 49 | 13400 (177); 12500 (153); 13500 (88); 12400 (65); 12600 (59) |
| ExposureTime | 901 | 1 | 10 (901) |
| AveragePulseWidth | 901 | 45 | 18 (201); 15 (178); 62 (110); 20 (96); 61 (81) |
| RadiationSetting | 901 | 1 | SC (901) |
| RadiationMode | 901 | 1 | PULSED (901) |
| ShutterShape | 901 | 1 | RECTANGULAR (901) |
| ShutterLeftVerticalEdge | 901 | 1 | 0 (901) |
| ShutterRightVerticalEdge | 901 | 2 | 1024 (602); 2048 (299) |
| ShutterUpperHorizontalEdge | 901 | 1 | 0 (901) |
| ShutterLowerHorizontalEdge | 901 | 2 | 1024 (602); 2048 (299) |
| FieldOfViewShape | 901 | 1 |  (901) |
| NumberOfFrames | 901 | 1 | 1 (901) |
| RecommendedDisplayFrameRate | 901 | 1 | 30 (901) |
| PatientOrientation | 901 | 1 |  (901) |
| BodyPartExamined | 901 | 1 | Entire body (901) |
| ProtocolName | 901 | 3 | 3 (602); 0 (298); 2 (1) |
| SeriesDescription | 901 | 1 | DR (901) |
| StationName | 901 | 1 | 922ea1912b (901) |
| DeviceSerialNumber | 901 | 1 | 9debf14c81 (901) |

Identity tags present (values never copied): {'PatientName': 901, 'PatientID': 901, 'PatientBirthDate': 901, 'InstitutionName': 901, 'ReferringPhysicianName': 901, 'OperatorsName': 600, 'InstitutionAddress': 901, 'PatientSex': 901}

## Private tags

Private creators: []

| tag creator VR | n | distinct | values |
|---|---:|---:|---|
| (0029,0016)  LO | 901 | 149 | 1895112604_20231112.150124.666 (304); 1895112604_20231111.151002.079 (303); 1895112604_20231212.112909.573 (2); 1895112604_20231211.175103.511 (2) |
| (0029,0020)  LO | 380 | 5 | - (301);  (76);  (1);  (1) |
| (0029,0020)  UL | 521 | 2 | 301 (301); 1 (220) |
| (0029,0021)  LO | 380 | 269 | � (30); � (20); � (10); � (8) |
| (0029,0021)  UL | 521 | 482 | 73063 (3); 73054 (3); 1375 (3); 1481 (3) |
| (0029,0022)  LO | 380 | 227 | � (49); �' (17); � (12); � (11) |
| (0029,0022)  UL | 521 | 484 | 33800 (3); 33807 (3); 33811 (3); 681 (3) |
| (0029,0023)  LO | 380 | 1 |  (380) |
| (0029,0023)  US | 521 | 1 | 14 (521) |
| (0029,0024)  LO | 380 | 1 |  (380) |
| (0029,0024)  UL | 521 | 1 | 1 (521) |
| (0029,0025)  LO | 901 | 1 | 通用 (901) |
| (0029,0026)  LO | 380 | 1 |  (380) |
| (0029,0026)  US | 521 | 1 | 0 (521) |
| (0029,0027)  LO | 380 | 1 |  (380) |
| (0029,0027)  US | 521 | 1 | 0 (521) |
| (0029,0028)  LO | 380 | 1 | * (380) |
| (0029,0028)  US | 521 | 1 | 42 (521) |
| (0029,0029)  LO | 380 | 1 |  (380) |
| (0029,0029)  US | 521 | 1 | 21 (521) |
| (0029,0030)  LO | 901 | 1 | 0.0 (901) |
| (0029,0031)  LO | 901 | 1 | 0 (901) |
| (0029,0032)  LO | 901 | 1 | 0 (901) |
| (0029,0033)  LO | 901 | 1 | 30cm (901) |
| (0029,0050)  LO | 901 | 5 | 46 (304); 40 (303); 33 (218); 21 (60) |
| (0029,0051)  LO | 901 | 4 | 89 (607); 27 (218); 115 (74); 88 (2) |
| (0029,0052)  LO | 901 | 123 | 900 (138); 0 (130); 1 (16); 899 (11) |
| (0029,0053)  LO | 901 | 8 | 9 (312); 6 (280); 0 (131); 1 (83) |
| (0029,0054)  LO | 901 | 1 | 0 (901) |
| (0029,0061)  LO | 380 | 1 |  (380) |
| (0029,0061)  LT | 521 | 1 |  (521) |
| (0029,0063)  LO | 901 | 2 | LSH (602); LIH (299) |
| (0035,0071)  LO | 901 | 1 | 1 (901) |
| (0035,0081)  LO | 380 | 2 |  (301);  (79) |
| (0035,0081)  US | 521 | 2 | 3 (301); 1 (220) |
| (0035,0082)  LO | 380 | 2 |  (378);  (2) |
| (0035,0082)  US | 521 | 2 | 1 (511); 0 (10) |
| (0037,0010)  LO | 301 | 1 | , (301) |
| (0037,0010)  US | 301 | 1 | 300 (301) |
| (0037,0011)  FD | 301 | 1 | 0.69 (301) |
| (0037,0011)  LO | 301 | 1 | 呺Q�呺? (301) |
| (0037,0013)  LO | 301 | 1 |  (301) |
| (0037,0013)  US | 301 | 1 | 7 (301) |
| (0037,0014)  LO | 602 | 1 | C:/FICBCT/IRayJupi1212X/FICBCT_3DC_110kv_300_FDK_noSC_AutoMAR_fR...(75) (602) |
| (0037,0015)  LO | 301 | 1 |  (301) |
| (0037,0015)  US | 301 | 1 | 1 (301) |
| (0037,0020)  LO | 301 | 264 | ��������������������������������...(2097152) (30); ��������������������������������...(2097152) (9); ���qpp^v|jgt����wud����uz�{y�lfc...(2092690) (1); ���������������������}������t�q�...(2090970) (1) |
| (0037,0020)  OW | 301 | 1 | <2097152 bytes> (301) |
