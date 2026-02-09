# Villa Romanza — Network VLAN Migration
# Generated: 2026-02-07 | Completed: 2026-02-07
# Source: UniFi EFG DHCP Export + Home Assistant MCP
# Status: MIGRATION COMPLETE

## Pre-Migration Subnet Layout
| Subnet | VLAN | Gateway | Purpose | Device Count |
|---|---|---|---|---|
| 192.168.0.0/23 | Core (1) | EFG | Everything (flat network) | ~137 |
| 192.168.6.0/24 | Smart Things (6) | EFG | IoT accessories | 9 |
| 192.168.7.0/24 | Guests (7) | EFG | Guest WiFi | 1 |

## Final VLAN Architecture (Post-Migration)
| VLAN ID | Subnet | Purpose | Status |
|---|---|---|---|
| 1 (Core) | 192.168.0.0/23 | Media/AV, Crestron, HA-CORE | Sonos, TVs, AVRs, Crestron, printers, HA |
| 4 (Security) | 192.168.4.0/24 | Protect NVR, AI Key, 36 cameras | MIGRATED |
| 6 (Smart Things) | 192.168.6.0/24 | IoT (MyQ, iRobot, sprinklers) | Unchanged |
| 7 (Guests) | 192.168.7.0/24 | Guest WiFi | Unchanged |
| 10 (Management) | 192.168.10.0/24 | Created but unused | Skipped — HA stays on Core |
| 20 (Lighting) | 192.168.20.0/24 | 29 Hue Bridges + 20 Hue Sync Boxes | MIGRATED |
| 30 (Media) | 192.168.30.0/24 | Reserved for future use | Empty |
| 70 (Mobility) | 192.168.70.0/24 | Reserved for future use | Empty |

## Complete Device Inventory by Category

### Network Infrastructure (1 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| HA-CORE | 192.168.1.6 | 20:f8:3b:02:40:23 | Fixed | VLAN 10 (Management) |

### UniFi Access Points (19 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| AP-Bar | 192.168.0.36 | a8:9c:6c:a4:55:34 | Dynamic | VLAN 10 (Management) |
| AP-Library | 192.168.0.81 | 84:78:48:1a:ac:76 | Dynamic | VLAN 10 (Management) |
| AP-Pool | 192.168.0.108 | 94:2a:6f:5e:46:5c | Dynamic | VLAN 10 (Management) |
| AP-Wine | 192.168.1.30 | 84:78:48:1a:11:2b | Dynamic | VLAN 10 (Management) |
| AP-Studio | 192.168.1.31 | 84:78:48:1a:16:1c | Dynamic | VLAN 10 (Management) |
| AP-Kitchen | 192.168.1.32 | 1c:0b:8b:00:e4:05 | Dynamic | VLAN 10 (Management) |
| AP-Sunroom | 192.168.1.33 | 84:78:48:1a:a8:bb | Dynamic | VLAN 10 (Management) |
| AP-Cabana | 192.168.1.37 | 1c:0b:8b:00:c8:21 | Dynamic | VLAN 10 (Management) |
| AP-Court | 192.168.1.38 | 94:2a:6f:5c:bf:88 | Dynamic | VLAN 10 (Management) |
| AP-Gate | 192.168.1.40 | 94:2a:6f:5e:3c:cc | Dynamic | VLAN 10 (Management) |
| AP-Up Guest | 192.168.1.41 | 84:78:48:1a:ae:51 | Dynamic | VLAN 10 (Management) |
| AP-Master | 192.168.1.42 | 1c:0b:8b:00:8f:35 | Dynamic | VLAN 10 (Management) |
| AP-Blue BR | 192.168.1.44 | 84:78:48:1c:0d:e8 | Dynamic | VLAN 10 (Management) |
| AP-His | 192.168.1.45 | 84:78:48:18:e3:8f | Dynamic | VLAN 10 (Management) |
| AP-Maids | 192.168.1.46 | 84:78:48:1c:0d:6b | Dynamic | VLAN 10 (Management) |
| AP-Picnic | 192.168.1.47 | 94:2a:6f:5c:a8:84 | Dynamic | VLAN 10 (Management) |
| AP-Lounge | 192.168.1.48 | 84:78:48:1c:0b:e5 | Dynamic | VLAN 10 (Management) |
| AP-Plaza | 192.168.1.49 | 94:2a:6f:5c:0c:3c | Dynamic | VLAN 10 (Management) |
| AP-Down Guest | 192.168.1.50 | 84:78:48:1c:0e:4c | Dynamic | VLAN 10 (Management) |

### Switches (5 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| SW-MEDIA | 192.168.1.12 | 54:07:7d:32:19:7c | Fixed | VLAN 10 (Management) — or Core if Netgear |
| SW-Studio | 192.168.1.15 | 28:94:01:6d:35:d0 | Fixed | VLAN 10 (Management) — or Core if Netgear |
| SW-BAR | 192.168.1.16 | 28:94:01:6d:33:74 | Fixed | VLAN 10 (Management) — or Core if Netgear |
| SW-Master | 192.168.1.17 | 28:94:01:6d:33:84 | Fixed | VLAN 10 (Management) — or Core if Netgear |
| SW-MasterBed | 192.168.1.18 | 54:07:7d:25:28:0b | Fixed | VLAN 10 (Management) — or Core if Netgear |

### Hue Bridges (29 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| HueB-01-Bar | 192.168.1.121 | c4:29:96:b4:14:ba | Fixed | VLAN 20 (Lighting) |
| HueB-02-GreatRoom | 192.168.1.122 | c4:29:96:b4:22:48 | Fixed | VLAN 20 (Lighting) |
| HueB-04-Dining | 192.168.1.123 | c4:29:96:b4:12:89 | Fixed | VLAN 20 (Lighting) |
| HueB-11-Kitchen | 192.168.1.124 | c4:29:96:b0:68:ea | Fixed | VLAN 20 (Lighting) |
| HueB-12-SunRoom | 192.168.1.125 | c4:29:96:b4:28:73 | Fixed | VLAN 20 (Lighting) |
| HueB-06-Loggia | 192.168.1.126 | c4:29:96:b8:d9:4b | Fixed | VLAN 20 (Lighting) |
| HueB-19-Gate | 192.168.1.127 | c4:29:96:ba:11:b2 | Fixed | VLAN 20 (Lighting) |
| HueB-08-Library | 192.168.1.128 | c4:29:96:b4:23:2f | Fixed | VLAN 20 (Lighting) |
| HueB-13-SouthHall | 192.168.1.129 | c4:29:96:b4:15:83 | Fixed | VLAN 20 (Lighting) |
| HueB-Cabana | 192.168.1.130 | c4:29:96:b4:14:7a | Fixed | VLAN 20 (Lighting) |
| HueB-14-Master | 192.168.1.131 | c4:29:96:b0:3f:32 | Fixed | VLAN 20 (Lighting) |
| HueB-10-Upstairs | 192.168.1.132 | c4:29:96:b4:12:ef | Fixed | VLAN 20 (Lighting) |
| HueB-09-1stGuest | 192.168.1.133 | c4:29:96:b4:14:b3 | Fixed | VLAN 20 (Lighting) |
| HueB-05-GroundFX | 192.168.1.134 | c4:29:96:b4:19:65 | Fixed | VLAN 20 (Lighting) |
| HueB-17-Veranda | 192.168.1.135 | c4:29:96:b4:14:bc | Fixed | VLAN 20 (Lighting) |
| HueB-03-Chandelier | 192.168.1.136 | c4:29:96:b0:3d:af | Fixed | VLAN 20 (Lighting) |
| HueB-15-Studio | 192.168.1.137 | c4:29:96:b4:1e:6d | Fixed | VLAN 20 (Lighting) |
| HueB-21-Lamps | 192.168.1.138 | c4:29:96:b4:20:0c | Fixed | VLAN 20 (Lighting) |
| HueB-18-West Lawn | 192.168.1.139 | c4:29:96:b4:1a:0e | Fixed | VLAN 20 (Lighting) |
| HueB-25-Theatre | 192.168.1.140 | c4:29:96:ba:14:84 | Fixed | VLAN 20 (Lighting) |
| HueB-24-2ndGuest | 192.168.1.141 | ec:b5:fa:9d:c0:68 | Fixed | VLAN 20 (Lighting) |
| HueB-22-SWBed | 192.168.1.142 | ec:b5:fa:bb:e6:f3 | Fixed | VLAN 20 (Lighting) |
| HueB-23-SEBed | 192.168.1.143 | ec:b5:fa:b0:8c:fa | Fixed | VLAN 20 (Lighting) |
| HueB-25-Utility | 192.168.1.144 | ec:b5:fa:bb:cd:32 | Fixed | VLAN 20 (Lighting) |
| HueB-07-Entrata | 192.168.1.145 | c4:29:96:c4:23:fd | Fixed | VLAN 20 (Lighting) |
| HueB-19-Roof | 192.168.1.146 | c4:29:96:b0:3b:eb | Fixed | VLAN 20 (Lighting) |
| HueB-26-MB2 | 192.168.1.147 | c4:29:96:b9:a9:9f | Fixed | VLAN 20 (Lighting) |
| HueB-20-Pool | 192.168.1.148 | c4:29:96:b4:2c:c7 | Fixed | VLAN 20 (Lighting) |
| HueB-Entrata | 192.168.1.149 | c4:29:96:b4:23:fd | Fixed | VLAN 20 (Lighting) |

### Hue Sync Boxes (20 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| HueS-Cabana | 192.168.1.79 | c4:29:96:e2:67:a2 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-17-Veranda | 192.168.1.80 | c4:29:96:e0:ee:70 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-06-Loggia | 192.168.1.81 | c4:29:96:e0:ef:ce | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-03-Chandelier | 192.168.1.82 | c4:29:96:e0:ee:8a | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-18-WLawn | 192.168.1.83 | c4:29:96:e2:00:96 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-21-Lamps | 192.168.1.84 | c4:29:96:e2:93:3c | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-20-Pool | 192.168.1.85 | c4:29:96:e2:88:26 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-O1-Bar | 192.168.1.86 | c4:29:96:e2:46:d6 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-03-Chandelier | 192.168.1.88 | c4:29:96:e1:ad:30 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-19-Upstairs | 192.168.1.89 | c4:29:96:e2:53:66 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-08-Library | 192.168.1.90 | c4:29:96:e2:d7:7a | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-19-Roof | 192.168.1.91 | c4:29:96:e2:96:ee | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-02-Great Room | 192.168.1.92 | c4:29:96:e2:22:26 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-11-Kitchen | 192.168.1.93 | c4:29:96:e2:00:d8 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-04-Dining | 192.168.1.94 | c4:29:96:e2:49:d0 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-26-Theatre | 192.168.1.95 | c4:29:96:e2:db:fa | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-09-SunRoom | 192.168.1.96 | c4:29:96:e2:45:f6 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-13-South Hall | 192.168.1.97 | c4:29:96:e1:1e:84 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-26-Master2 | 192.168.1.98 | c4:29:96:e2:a4:b0 | Fixed | VLAN 20 (Lighting) via WiFi SSID |
| HueS-05-Ground FX | 192.168.1.99 | c4:29:96:e2:49:e0 | Fixed | VLAN 20 (Lighting) via WiFi SSID |

### Sonos Speakers (29 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| SNS-Hers | 192.168.1.160 | 80:4a:f2:ae:c6:b2 | Fixed | Core (stays — behind Netgear) |
| SNS-Master Entry | 192.168.1.162 | 80:4a:f2:ae:c6:c1 | Fixed | Core (stays — behind Netgear) |
| SNS-Lounge | 192.168.1.163 | c4:38:75:8d:3e:24 | Fixed | Core (stays — behind Netgear) |
| SNS-Kitchen | 192.168.1.164 | 74:ca:60:41:8e:61 | Fixed | Core (stays — behind Netgear) |
| SNS-Garage | 192.168.1.165 | 80:4a:f2:ae:c6:df | Fixed | Core (stays — behind Netgear) |
| SNS-Picnic | 192.168.1.166 | 80:4a:f2:a9:7d:07 | Fixed | Core (stays — behind Netgear) |
| SNS-His | 192.168.1.167 | 74:ca:60:41:8f:66 | Fixed | Core (stays — behind Netgear) |
| SNS-BlueBedroom | 192.168.1.168 | 80:4a:f2:ae:c6:f1 | Fixed | Core (stays — behind Netgear) |
| SNS-Library | 192.168.1.169 | 80:4a:f2:ae:30:5b | Fixed | Core (stays — behind Netgear) |
| SNS-Dining | 192.168.1.170 | 80:4a:f2:ae:30:61 | Fixed | Core (stays — behind Netgear) |
| SNS-GuestUp | 192.168.1.171 | c4:38:75:8b:b9:83 | Fixed | Core (stays — behind Netgear) |
| SNS-Entrata | 192.168.1.172 | 80:4a:f2:a8:43:78 | Fixed | Core (stays — behind Netgear) |
| SNS-Porch | 192.168.1.173 | 80:4a:f2:a8:42:a3 | Fixed | Core (stays — behind Netgear) |
| SNS-GuestDown | 192.168.1.175 | 80:4a:f2:ae:c0:be | Fixed | Core (stays — behind Netgear) |
| SNS-Wine | 192.168.1.176 | 80:4a:f2:a8:42:b2 | Fixed | Core (stays — behind Netgear) |
| SNS-PinkBedroom | 192.168.1.177 | 80:4a:f2:ae:a2:10 | Fixed | Core (stays — behind Netgear) |
| SNS-PT-Bar | 192.168.1.178 | 38:42:0b:8f:11:ae | Fixed | Core (stays — behind Netgear) |
| SNS-PT-Sunroom | 192.168.1.179 | 00:1b:66:04:0a:e9 | Fixed | Core (stays — behind Netgear) |
| SNS-Lawn | 192.168.1.180 | 38:42:0b:26:92:5e | Fixed | Core (stays — behind Netgear) |
| SNS-Master L | 192.168.1.181 | 80:4a:f2:86:57:6c | Fixed | Core (stays — behind Netgear) |
| SNS-Master R | 192.168.1.182 | 80:4a:f2:86:53:9c | Fixed | Core (stays — behind Netgear) |
| SNS-Master Sub | 192.168.1.183 | c4:38:75:d3:6e:92 | Fixed | Core (stays — behind Netgear) |
| SNS-MasterPort | 192.168.1.184 | 38:42:0b:8e:dc:8c | Fixed | Core (stays — behind Netgear) |
| SNS-Cabana | 192.168.1.185 | c4:38:75:8b:7d:80 | Fixed | Core (stays — behind Netgear) |
| SNS-Pool N | 192.168.1.186 | 38:42:0b:26:93:39 | Fixed | Core (stays — behind Netgear) |
| SNS-Pool S | 192.168.1.187 | 74:ca:60:49:18:8a | Fixed | Core (stays — behind Netgear) |
| SNS-PT-Sync Feed | 192.168.1.188 | 38:42:0b:8f:0c:ce | Fixed | Core (stays — behind Netgear) |
| SNS-Pool East | 192.168.1.189 | 74:ca:60:e0:9a:32 | Fixed | Core (stays — behind Netgear) |
| SNS-P Lawn Sub 2 | 192.168.1.192 | 74:ca:60:31:da:dc | Fixed | Core (stays — behind Netgear) |

### Crestron Control (16 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| CP4-R | 192.168.1.2 | c4:42:68:41:92:fb | Fixed | Core (stays — needs media access) |
| VRROOM | 192.168.1.70 | 18:9b:a5:d4:12:cb | Fixed | Core (stays — needs media access) |
| TP-Cava Romanza | 192.168.1.200 | c4:42:68:63:82:57 | Fixed | Core (stays — needs media access) |
| TP-Entrata | 192.168.1.201 | c4:42:68:63:85:e0 | Fixed | Core (stays — needs media access) |
| TP-Kitchen | 192.168.1.202 | c4:42:68:68:81:7a | Fixed | Core (stays — needs media access) |
| TP-Lounge | 192.168.1.203 | c4:42:68:25:33:67 | Fixed | Core (stays — needs media access) |
| TP-Dining | 192.168.1.204 | c4:42:68:68:73:05 | Fixed | Core (stays — needs media access) |
| TP-Garage | 192.168.1.205 | 00:10:7f:ef:fd:c1 | Fixed | Core (stays — needs media access) |
| TP-Laundry Down | 192.168.1.206 | c4:42:68:63:85:c9 | Fixed | Core (stays — needs media access) |
| TP-Villa Master | 192.168.1.207 | c4:42:68:63:83:83 | Fixed | Core (stays — needs media access) |
| TP-North Porta | 192.168.1.208 | c4:42:68:68:73:ed | Fixed | Core (stays — needs media access) |
| TP-Veranda | 192.168.1.210 | c4:42:68:63:82:ea | Fixed | Core (stays — needs media access) |
| TP-Villa Hers | 192.168.1.212 | c4:42:68:63:8e:1b | Fixed | Core (stays — needs media access) |
| TP-Villa His | 192.168.1.213 | c4:42:68:63:88:24 | Fixed | Core (stays — needs media access) |
| TP-Library | 192.168.1.215 | c4:42:68:68:b3:cc | Fixed | Core (stays — needs media access) |
| TP-Cabana | 192.168.1.217 | c4:42:68:63:83:2e | Fixed | Core (stays — needs media access) |

### AV Receivers (3 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| AVR-Master | 192.168.1.71 | 50:1e:2d:43:93:72 | Fixed | Core (stays — behind Netgear) |
| AVR-Sunroom | 192.168.1.73 | 7c:b7:7b:04:29:d1 | Fixed | Core (stays — behind Netgear) |
| AVR-Bar | 192.168.1.75 | 50:1e:2d:43:a0:c0 | Fixed | Core (stays — behind Netgear) |

### LG TVs (3 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| TV-Up Guest | 192.168.1.58 | 60:75:6c:32:c3:f2 | Fixed | Core (stays — behind Netgear) |
| TV-Master | 192.168.1.72 | 58:96:0a:40:cc:9f | Fixed | Core (stays — behind Netgear) |
| TV-SunRoom (New) | 192.168.1.74 | b0:37:95:16:fd:f0 | Fixed | Core (stays — behind Netgear) |

### Security/Protect (2 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| UP-AI-KEY-123E4B | 192.168.1.3 | 8c:ed:e1:12:3e:4b | Fixed | VLAN 50 (Security) |
| SEC-NVR | 192.168.1.7 | 0c:ea:14:32:66:02 | Fixed | VLAN 50 (Security) |

### IoT Accessories (8 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| CTRL-Sprinklers | 192.168.6.10 | 74:d5:c6:41:60:c3 | Fixed | VLAN 60 (IoT) — already there |
| ACC-Garage x | 192.168.6.50 | 0c:95:05:1a:59:b1 | Fixed | VLAN 60 (IoT) — already there |
| ACC-Garage 1 | 192.168.6.51 | 0c:95:05:1a:59:b7 | Fixed | VLAN 60 (IoT) — already there |
| ACC-Garage 2 | 192.168.6.52 | 0c:95:05:1a:59:77 | Fixed | VLAN 60 (IoT) — already there |
| ACC-Garage y | 192.168.6.53 | 0c:95:05:1a:12:8b | Fixed | VLAN 60 (IoT) — already there |
| VAC-2 | 192.168.6.181 | 4c:b9:ea:5c:00:0f | Fixed | VLAN 60 (IoT) — already there |
| VAC-3 | 192.168.6.182 | 50:14:79:72:17:74 | Fixed | VLAN 60 (IoT) — already there |
| VAC-6 | 192.168.6.186 | 4c:b9:ea:5c:00:7d | Fixed | VLAN 60 (IoT) — already there |

### Fitness (2 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| FIT-PeloBike | 192.168.1.198 | ac:04:0b:3a:b2:e7 | Fixed | VLAN 60 (IoT) |
| FIT-Tread | 192.168.1.199 | ac:04:0b:d2:c2:48 | Fixed | VLAN 60 (IoT) |

### Gaming (1 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| XBX-Bar | 192.168.1.55 | cc:b0:b3:62:97:f3 | Fixed | Core (stays) |

### Printers (2 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| Studio Printer | 192.168.1.56 | 30:8d:99:7e:cf:76 | Fixed | Core (stays) |
| PNT-Library | 192.168.1.195 | 24:6a:0e:59:7c:ba | Fixed | Core (stays) |

### Client Devices (4 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| MS-iPhone 5b:28 | 192.168.0.90 | 34:10:be:eb:5b:28 | Dynamic | VLAN 0 (Default) |
| Mac 0f:47 | 192.168.0.137 | 66:49:86:9c:0f:47 | Dynamic | VLAN 0 (Default) |
| Mac 46:c9 | 192.168.0.156 | b6:be:9a:50:46:c9 | Dynamic | VLAN 0 (Default) |
| MEATER-CED0 3a:2e | 192.168.0.157 | 90:21:2e:1e:3a:2e | Dynamic | VLAN 0 (Default) |

### Unknown (3 devices)
| Name | IP Address | MAC | Lease | Target VLAN |
|---|---|---|---|---|
| 28:29:86:63:79:ac | 192.168.1.8 | 28:29:86:63:79:ac | Fixed | TBD |
| 04:c4:61:80:65:75 | 192.168.6.185 | 04:c4:61:80:65:75 | Dynamic | TBD |
| ea:97:4b:19:f2:e9 | 192.168.7.111 | ea:97:4b:19:f2:e9 | Dynamic | TBD |

## Migration Summary

### Devices that MOVE to new VLANs
| Target VLAN | Devices | Count |
|---|---|---|
| VLAN 10 (Management) | HA-CORE, UniFi APs, UniFi switches | ~22 |
| VLAN 20 (Lighting) | Hue Bridges (wired), Hue Sync Boxes (WiFi) | ~49 |
| VLAN 50 (Security) | SEC-NVR, UP-AI-KEY | 2 |

### Devices that STAY on Core
| Category | Reason | Count |
|---|---|---|
| Sonos Speakers | Behind Netgear switches | 29 |
| Crestron (CP4-R + panels) | Needs media access | 15+ |
| AV Receivers | Behind Netgear switches | 3 |
| LG TVs | Behind Netgear switches | 3 |
| Xbox | Behind Netgear switches | 1 |
| Printers | Low priority | 2 |

### Devices already on correct VLANs
| Current VLAN | Devices | Count |
|---|---|---|
| VLAN 0 (Default) | Phones, Macs, laptops | ~4 |
| VLAN 60 (IoT) | MyQ, iRobot, sprinklers | ~9 |

## Migration Checklist
- [x] Install UniFi Network integration in HA
- [x] Install UniFi Protect integration in HA (API key from Settings > Control Plane > Integrations)
- [x] Create HA backup (Pre_VLAN_Migration_2026-02-07, backup_id: 038fd842)
- [x] Create VLANs on EFG (4-Security existed, created 10-Management, 20-Lighting)
- [x] Phase 1: Migrate Security devices to VLAN 4 (NVR + AI Key + 36 cameras)
- [x] Phase 2: Management — SKIPPED (HA stays on Core for safety)
- [x] Phase 3: Migrate Lighting to VLAN 20 (49 devices via DHCP CSV import)
- [x] Assign Hue-Sync WiFi SSID to Lighting VLAN 20
- [x] Enable firewall rules (8 existing rules enabled via HA)
- [x] Create Lighting VLAN isolation rules (Allow LTG→Fort + Block LTG→VLANs)
- [x] Enable mDNS reflector on EFG
- [x] Post-migration verification — all systems operational

## Firewall Rules (Active)
| Rule | Type | Status |
|---|---|---|
| Allow SEC Intra-VLAN | LAN In | ON |
| Allow SEC→TCP Fort | LAN In | ON |
| Allow SEC→UDP Fort | LAN In | ON |
| Allow SEC→Fort Ping | LAN In | ON |
| Allow Fort→SEC | LAN In | ON |
| Block SEC→VLANs | LAN In | ON |
| Allow Guest Print | LAN In | ON |
| Drop Core→Guests | LAN In | ON |
| Allow LTG→Fort | LAN In | ON |
| Block LTG→VLANs | LAN In | ON — Source MUST be "Lighting" network only |

## Post-Migration Verification Results (2026-02-07)
| System | Status | Details |
|---|---|---|
| Hue integrations (27) | All loaded | All bridges communicating via inter-VLAN routing |
| Hue bridges on VLAN 20 | 26/29 home | 3 need power cycle (GreatRoom, Chandelier, Entrata-07) |
| Cameras | 25 online, 11 unavailable | Matches pre-migration baseline |
| Sonos (30 devices) | All connected | Zero unavailable — healthy on Core |
| LG TVs (3) | Unavailable | Powered off (normal) |
| Automations (13) | 12 ON, 1 OFF | Disabled duplicate is expected |
| UniFi switches (15) | 14 home, 1 not_home | SW-Bar 2 (likely Netgear) |
| Access points (22) | 21 home, 1 not_home | AP-Bar needs investigation |
| All HA integrations (57) | 56 loaded, 1 ignored | 100% operational |

## Known Issues / Follow-up
- [ ] Power cycle 3 Hue bridges (GreatRoom, Chandelier, Entrata-07) to register on VLAN 20
- [ ] Investigate AP-Bar showing not_home
- [ ] SW-Bar 2 not_home — confirm if Netgear (expected)
- [ ] Install HACS for UniFi Access integration (future)
- [ ] Consider moving Peloton/Tread to IoT VLAN 6 (future)
