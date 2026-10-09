# Philips Medical Systems | AlluraXper — header census

590 DICOM headers under `/rs/rs_grp_oschome/go2432/data/spinesac/drive` (samples: 2d_3dRL dataset/GE/SCN 1/Output1/AP/IP/APFlip.dcm, 2d_3dRL dataset/GE/SCN 1/Output1/AP/IP/APIP.dcm, 2d_3dRL dataset/GE/SCN 1/Output1/AP/IP/L4.dcm, 2d_3dRL dataset/GE/SCN 1/Output1/LP/IP/LPFlip.dcm, 2d_3dRL dataset/GE/SCN 1/Output1/LP/IP/LPIP.dcm).

## Exposure and geometry (per frame)

| field | n | min | p5 | median | p95 | max |
|---|---:|---:|---:|---:|---:|---:|
| kvp | 590 | 80 | 80 | 80 | 80 | 80 |
| sid_mm | 590 | 1195 | 1195 | 1195 | 1195 | 1195 |
| sod_mm | 590 | 810 | 810 | 810 | 810 | 810 |
| primary_deg | 590 | -0.24 | -0.24 | -0.24 | -0.24 | -0.24 |
| secondary_deg | 590 | -2.4 | -2.4 | -2.4 | -2.4 | -2.4 |
| imager_pixel_mm | 590 | 0.7418 | 0.7418 | 0.7418 | 0.7418 | 0.7418 |

## Public tags

| tag | n | distinct | most common values (count) |
|---|---:|---:|---|
| Manufacturer | 590 | 1 | Philips Medical Systems (590) |
| ManufacturerModelName | 590 | 1 | AlluraXper (590) |
| SoftwareVersions | 590 | 1 | Allura Xper, 8.1.17.2 (590) |
| Modality | 590 | 1 | XA (590) |
| ImageType | 590 | 1 | ORIGINAL\PRIMARY\SINGLE PLANE\SINGLE A (590) |
| SOPClassUID | 590 | 1 | 1.2.840.10008.5.1.4.1.1.12.1 (590) |
| Rows | 590 | 13 | 1024 (383); 1002 (86); 970 (66); 512 (35); 250 (6) |
| Columns | 590 | 15 | 1052 (266); 1024 (166); 1035 (53); 1003 (43); 512 (35) |
| BitsAllocated | 590 | 2 | 16 (476); 8 (114) |
| BitsStored | 590 | 2 | 16 (476); 8 (114) |
| HighBit | 590 | 2 | 15 (476); 7 (114) |
| PixelRepresentation | 590 | 1 | 0 (590) |
| PhotometricInterpretation | 590 | 1 | MONOCHROME2 (590) |
| PixelIntensityRelationship | 590 | 1 | LIN (590) |
| WindowCenter | 590 | 3 | 124.5 (540); 32767.5 (28); 127.5 (22) |
| WindowWidth | 590 | 3 | 170.75 (540); 65535 (28); 255 (22) |
| ImagerPixelSpacing | 590 | 1 | 0.74181640625\0.74181640625 (590) |
| DistanceSourceToDetector | 590 | 1 | 1195 (590) |
| DistanceSourceToPatient | 590 | 1 | 810 (590) |
| PositionerPrimaryAngle | 590 | 1 | -0.24 (590) |
| PositionerSecondaryAngle | 590 | 1 | -2.4 (590) |
| KVP | 590 | 1 | 80 (590) |
| RadiationSetting | 590 | 1 | GR (590) |
| ShutterShape | 590 | 1 | RECTANGULAR (590) |
| ShutterLeftVerticalEdge | 590 | 1 | 69 (590) |
| ShutterRightVerticalEdge | 590 | 1 | 448 (590) |
| ShutterUpperHorizontalEdge | 590 | 1 | 1 (590) |
| ShutterLowerHorizontalEdge | 590 | 1 | 512 (590) |
| LossyImageCompression | 590 | 1 | 00 (590) |
| PatientOrientation | 590 | 1 |  (590) |
| TableMotion | 590 | 1 | STATIC (590) |
| ProtocolName | 590 | 1 | Head (590) |
| PerformedProcedureStepDescription | 590 | 1 | Head 3D (590) |
| SeriesDescription | 590 | 1 | Cerebral Single Shot (590) |
| StationName | 590 | 1 | 386ceeeebc (590) |
| DeviceSerialNumber | 590 | 1 | 386ceeeebc (590) |
| VOILUTFunction | 50 | 1 | LINEAR (50) |

Identity tags present (values never copied): {'PatientName': 590, 'PatientID': 590, 'PatientBirthDate': 590, 'InstitutionName': 590, 'ReferringPhysicianName': 590, 'PatientSex': 590}

## Private tags

Private creators: [('Philips X-ray Imaging DD 001', 946), ('Philips X-ray Imaging DD 003', 817), ('Philips Imaging DD 001', 86), (828, 86), (58, 43)]

| tag creator VR | n | distinct | values |
|---|---:|---:|---|
| (2001,0000)  UL | 43 | 1 | 58 (43) |
| (2001,0010) 58 LO | 43 | 1 | Philips Imaging DD 001 (43) |
| (2001,1063) Philips Imaging DD 001 CS | 43 | 1 | ELSEWHERE (43) |
| (2001,10a1) Philips Imaging DD 001 CS | 43 | 1 | NO (43) |
| (2003,0000)  UL | 43 | 1 | 828 (43) |
| (2003,0010) 828 LO | 43 | 1 | Philips X-ray Imaging DD 001 (43) |
| (2003,0012) 828 LO | 43 | 1 | Philips X-ray Imaging DD 003 (43) |
| (2003,1001) Philips X-ray Imaging DD 001 LO | 43 | 1 | Vascular (43) |
| (2003,1002) Philips X-ray Imaging DD 001 FD | 43 | 1 | 484.0\380.0\300.0 (43) |
| (2003,1003) Philips X-ray Imaging DD 001 LO | 43 | 1 | FD 48 cm (43) |
| (2003,1009) Philips X-ray Imaging DD 001 SL | 43 | 1 | 2 (43) |
| (2003,1010) Philips X-ray Imaging DD 001 LO | 43 | 1 | FD 48 cm (43) |
| (2003,1016) Philips X-ray Imaging DD 001 SL | 43 | 1 | 1 (43) |
| (2003,1017) Philips X-ray Imaging DD 001 SL | 43 | 1 | 1 (43) |
| (2003,1018) Philips X-ray Imaging DD 001 SL | 43 | 1 | 1 (43) |
| (2003,1019) Philips X-ray Imaging DD 001 SL | 43 | 1 | 0 (43) |
| (2003,1022) Philips X-ray Imaging DD 001 SL | 43 | 1 | 1 (43) |
| (2003,1024) Philips X-ray Imaging DD 001 FD | 43 | 1 | 60.0\1.0\454.0\512.0 (43) |
| (2003,1027) Philips X-ray Imaging DD 001 SH | 43 | 1 | UP (43) |
| (2003,1028) Philips X-ray Imaging DD 001 SH | 43 | 1 | DOWN (43) |
| (2003,1029) Philips X-ray Imaging DD 001 FD | 43 | 1 | 0.0 (43) |
| (2003,102a) Philips X-ray Imaging DD 001 LO | 43 | 1 | none (43) |
| (2003,102b) Philips X-ray Imaging DD 001 FD | 43 | 1 | -90.9 (43) |
| (2003,102c) Philips X-ray Imaging DD 001 SH | 43 | 1 | FRONTAL (43) |
| (2003,102d) Philips X-ray Imaging DD 001 SL | 43 | 1 | -1000 (43) |
| (2003,1030) Philips X-ray Imaging DD 001 CS | 43 | 1 | YES (43) |
| (2003,1031) Philips X-ray Imaging DD 001 CS | 43 | 1 | STANDARD (43) |
| (2003,1032) Philips X-ray Imaging DD 001 UI | 43 | 1 | 1.3.46.670589.28.681722601919398.20200226101214671337.2.2 (43) |
| (2003,1033) Philips X-ray Imaging DD 001 UL | 43 | 1 | 5 (43) |
| (2003,1201) Philips X-ray Imaging DD 003 IS | 43 | 1 | <1 bytes> (43) |
| (2003,1202) Philips X-ray Imaging DD 003 DS | 43 | 1 | 2.4 (43) |
| (2003,1203) Philips X-ray Imaging DD 003 DS | 43 | 1 | 0.2 (43) |
| (2003,1204) Philips X-ray Imaging DD 003 DS | 43 | 1 | -0.2 (43) |
| (2003,1205) Philips X-ray Imaging DD 003 DS | 43 | 1 | 1 (43) |
| (2003,1206) Philips X-ray Imaging DD 003 DS | 43 | 1 | -90.9 (43) |
| (2003,1207) Philips X-ray Imaging DD 003 DS | 43 | 1 | 1913 (43) |
| (2003,1208) Philips X-ray Imaging DD 003 DS | 43 | 1 | 1195 (43) |
| (2003,1209) Philips X-ray Imaging DD 003 DS | 43 | 1 | 810 (43) |
| (2003,1210) Philips X-ray Imaging DD 003 SH | 43 | 1 | UP (43) |
| (2003,1211) Philips X-ray Imaging DD 003 SH | 43 | 1 | DOWN (43) |
| (2003,1212) Philips X-ray Imaging DD 003 DS | 43 | 1 | 1039 (43) |
| (2003,1213) Philips X-ray Imaging DD 003 DS | 43 | 1 | 2533.4 (43) |
| (2003,1214) Philips X-ray Imaging DD 003 DS | 43 | 1 | -16.7 (43) |
| (2003,1215) Philips X-ray Imaging DD 003 DS | 43 | 1 | 0 (43) |
| (2003,1216) Philips X-ray Imaging DD 003 DS | 43 | 1 | 0.4 (43) |
| (2003,1217) Philips X-ray Imaging DD 003 DS | 43 | 1 | 0 (43) |
| (2003,1218) Philips X-ray Imaging DD 003 DS | 43 | 1 | 718.390625 (43) |
| (2003,1219) Philips X-ray Imaging DD 003 DS | 43 | 1 | 718.390625 (43) |
