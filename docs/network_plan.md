# Villa Romanza — Network Fixed IP & Lockdown Plan (FINAL)
# Updated: 2026-02-08
# Full reservation list: scratchpad/fixed_ip_reservations.md

---

## Core VLAN IP Address Map (192.168.0.0/23)

### Infrastructure (1.1-1.9) — Already Fixed
| IP | Device | MAC |
|---|---|---|
| 1.1 | VR The Mighty Fortress (EFG) | 28:70:4e:27:97:49 |
| 1.2 | CP4-R (Crestron) | c4:42:68:41:92:fb |
| 1.4 | SW-CORE | 84:78:48:60:15:b3 |
| 1.5 | PWR-PDU | 6c:63:f8:2e:84:c7 |
| 1.6 | HA-CORE (Home Assistant Green) | 20:f8:3b:02:40:23 |
| 1.9 | SW-SECURITY | 84:78:48:58:f7:11 |

### Switches (1.10-1.65) — Already Fixed
22+ switches, all with fixed IPs in UniFi.

### Access Points (1.30-1.50) — Already Fixed
22 APs. Note: AP-Library (.0.81), AP-Bar (.0.32), AP-Pool (.0.108) are on 0.x — inconsistent but reachable.

### VRROOM + Media Devices (1.70-1.81) — NEW RESERVATIONS
| IP | Device | Model | MAC | Location |
|---|---|---|---|---|
| **1.70** | **VRROOM** | Crestron DM-NVX | **18:9b:a5:d4:12:cb** | Machine Room |
| **1.71** | **TV-MasterCinema** | OLED77C5PUA 77" | **60:75:6c:32:c3:f2** | Master Cinema |
| **1.72** | **TV-Theatre** | OLED83C5PUA 83" | **58:96:0a:40:cc:9f** | Theatre (Bar) |
| **1.73** | **TV-DownGuest** | OLED48C5PUA 48" | **1c:f4:3f:0d:80:c4** | Down Guest |
| **1.74** | **TV-Sunroom** | OLED83G2PUA 83" | **b0:37:95:16:fd:f0** | Sunroom |
| **1.75** | TV-2ndGuest (DEFERRED) | OLED65G1PUA 65" | TBD | 2nd Floor Guest |
| **1.76** | **ATV-MasterCinema** | Apple TV | **c4:f7:c1:2b:09:68** | Master Cinema |
| **1.77** | **ATV-Theatre** | Apple TV | **c0:95:6d:58:1a:5d** | Theatre (Bar) |
| **1.78** | **TV-Cabana** | LG C5 2025 | **08:27:a8:23:50:62** | Cabana |
| **1.79** | **ATV-DownGuest** | Apple TV | **c4:f7:c1:12:c4:ba** | Down Guest |
| **1.80** | **ATV-Sunroom** | Apple TV | **f0:b3:ec:32:ed:c5** | Sunroom |
| **1.81** | **ATV-Cabana** | Apple TV | **f0:b3:ec:28:fa:60** | Cabana |

### Crestron Touch Panels (1.82-1.95) — NEW RESERVATIONS
| IP | Name | MAC |
|---|---|---|
| **1.82** | TP-Lounge | **c4:42:68:25:33:67** |
| **1.83** | TP-Entrata | **c4:42:68:63:85:e0** |
| **1.84** | TP-Kitchen | **c4:42:68:68:81:7a** |
| **1.85** | TP-VillaMaster | **c4:42:68:63:83:83** |
| **1.86** | TP-Cabana | **c4:42:68:63:83:2e** |
| **1.87** | TP-Garage | **00:10:7f:ef:fd:c1** |
| **1.88** | TP-VillaHis | **c4:42:68:63:88:24** |
| **1.89** | TP-CavaRomanza | **c4:42:68:63:82:57** |
| **1.90** | TP-Veranda | **c4:42:68:63:82:ea** |
| **1.91** | TP-Dining | **c4:42:68:68:73:05** |
| **1.92** | TP-VillaHers | **c4:42:68:63:8e:1b** |
| **1.93** | TP-LaundryDown | **c4:42:68:63:85:c9** |
| **1.94** | TP-NorthPorta | **c4:42:68:68:73:ed** |
| **1.95** | TP-Library | **c4:42:68:68:b3:cc** |

### Sonos Speakers (0.100-0.125) — NEW RESERVATIONS
| IP | Name | MAC |
|---|---|---|
| **0.100** | SNS-Library | **80:4a:f2:ae:30:5b** |
| **0.101** | SNS-Lounge | **c4:38:75:8d:3e:24** |
| **0.102** | SNS-Kitchen | **74:ca:60:41:8e:61** |
| **0.103** | SNS-Dining | **80:4a:f2:ae:30:61** |
| **0.104** | SNS-Entrata | **80:4a:f2:a8:43:78** |
| **0.106** | SNS-MasterEntry | **80:4a:f2:ae:c6:c1** |
| **0.107** | SNS-His | **74:ca:60:41:8f:66** |
| **0.105** | SNS-Hers | **80:4a:f2:ae:c6:b2** |
| **0.109** | SNS-BlueBedroom | **80:4a:f2:ae:c6:f1** |
| **0.110** | SNS-PinkBedroom | **80:4a:f2:ae:a2:10** |
| **0.111** | SNS-GuestUp | **c4:38:75:8b:b9:83** |
| **0.112** | SNS-GuestDown | **80:4a:f2:ae:c0:be** |
| **0.113** | SNS-Garage | **80:4a:f2:ae:c6:df** |
| **0.114** | SNS-Wine | **80:4a:f2:a8:42:b2** |
| **0.115** | SNS-Porch | **80:4a:f2:a8:42:a3** |
| **0.116** | SNS-Lawn | **38:42:0b:26:92:5e** |
| **0.117** | SNS-Picnic | **80:4a:f2:a9:7d:07** |
| **0.118** | SNS-PoolNorth | **38:42:0b:26:93:39** |
| **0.119** | SNS-PoolSouth | **74:ca:60:49:18:8a** |
| **0.120** | SNS-PoolEast | **74:ca:60:e0:9a:32** |
| **0.121** | SNS-Cabana | **c4:38:75:8b:7d:80** |
| **0.122** | SNS-PT-Bar | **38:42:0b:8f:11:ae** |
| **0.123** | SNS-PT-SyncFeed | **38:42:0b:8f:0c:ce** |
| **0.124** | SNS-PT-Sunroom | **00:1b:66:04:0a:e9** |
| **0.125** | SNS-PicnicSub | **74:ca:60:31:da:dc** |

### AVRs (0.130-0.132) — NEW RESERVATIONS
| IP | Name | Model | MAC |
|---|---|---|---|
| **0.130** | AVR-Bar | Anthem MRX 540 | **50:1e:2d:43:a0:c0** |
| **0.131** | AVR-Master | Anthem MRX 40 | **50:1e:2d:43:93:72** |
| **0.132** | AVR-Sunroom | Paradigm | **7c:b7:7b:04:29:d1** |

### Mac Minis (0.140-0.142) — NEW RESERVATIONS
| IP | Name | Role | MAC |
|---|---|---|---|
| **0.140** | Mech-Mac | LEA / Reasoning | **d0:11:e5:ed:43:d4** |
| 0.141 | FX-Mac (DEFERRED) | Audio→NDI | TBD |
| 0.142 | Show-Mac (DEFERRED) | TouchDesigner | TBD |

### Other (0.150+) — NEW RESERVATIONS
| IP | Name | MAC |
|---|---|---|
| **0.150** | PNT-Library (Printer) | **24:6a:0e:59:7c:ba** |
| **0.151** | Ramonas-iMac | **78:7b:8a:aa:e4:ba** |
| **0.155** | Villa Chime Plug | **58:d6:1f:1e:41:93** |

---

## Lighting VLAN 20 (192.168.20.0/24)

### Hue Bridges (20.10-20.38) — NEW RESERVATIONS
| IP | Name | MAC |
|---|---|---|
| **20.10** | HueB-01-Bar | **c4:29:96:b4:14:ba** |
| **20.11** | HueB-02-GreatRoom | **c4:29:96:b4:22:48** |
| **20.12** | HueB-03-Chandelier | **c4:29:96:b0:3d:af** |
| **20.13** | HueB-04-Dining | **c4:29:96:b4:12:89** |
| **20.14** | HueB-05-GroundFX | **c4:29:96:b4:19:65** |
| **20.15** | HueB-06-Loggia | **c4:29:96:b8:d9:4b** |
| **20.16** | HueB-07-Entrata | **c4:29:96:c4:23:fd** |
| **20.17** | HueB-08-Library | **c4:29:96:b4:23:2f** |
| **20.18** | HueB-09-1stGuest | **c4:29:96:b4:14:b3** |
| **20.19** | HueB-10-Upstairs | **c4:29:96:b4:12:ef** |
| **20.20** | HueB-11-Kitchen | **c4:29:96:b0:68:ea** |
| **20.21** | HueB-12-SunRoom | **c4:29:96:b4:28:73** |
| **20.22** | HueB-13-SouthHall | **c4:29:96:b4:15:83** |
| **20.23** | HueB-14-Master | **c4:29:96:b0:3f:32** |
| **20.24** | HueB-15-Studio | **c4:29:96:b4:1e:6d** |
| **20.25** | HueB-17-Veranda | **c4:29:96:b4:14:bc** |
| **20.26** | HueB-18-WestLawn | **c4:29:96:b4:1a:0e** |
| **20.27** | HueB-19-Gate | **c4:29:96:ba:11:b2** |
| **20.28** | HueB-19-Roof | **c4:29:96:b0:3b:eb** |
| **20.29** | HueB-20-Pool | **c4:29:96:b4:2c:c7** |
| **20.30** | HueB-21-Lamps | **c4:29:96:b4:20:0c** |
| **20.31** | HueB-22-SWBed | **ec:b5:fa:bb:e6:f3** |
| **20.32** | HueB-23-SEBed | **ec:b5:fa:b0:8c:fa** |
| **20.33** | HueB-24-2ndGuest | **ec:b5:fa:9d:c0:68** |
| **20.34** | HueB-25-Theatre | **c4:29:96:ba:14:84** |
| **20.35** | HueB-25-Utility | **ec:b5:fa:bb:cd:32** |
| **20.36** | HueB-26-MB2 | **c4:29:96:b9:a9:9f** |
| **20.37** | HueB-Cabana | **c4:29:96:b4:14:7a** |
| **20.38** | HueB-Entrata | **c4:29:96:b4:23:fd** |

### Hue Sync Boxes (20.79-20.99) — ALREADY ASSIGNED
21 units discovered with fixed IPs at 192.168.20.79-99:
| IP | Name | MAC |
|---|---|---|
| 20.79 | HueS-Cabana | c4:29:96:e2:67:a2 |
| 20.80 | HueS-17-Veranda | c4:29:96:e0:ee:70 |
| 20.81 | HueS-06-Loggia | c4:29:96:e0:ef:ce |
| 20.82 | HueS-03-Chandelier | c4:29:96:e0:ee:8a |
| 20.83 | HueS-18-WLawn | c4:29:96:e2:00:96 |
| 20.84 | HueS-21-Lamps | c4:29:96:e2:93:3c |
| 20.85 | HueS-20-Pool | c4:29:96:e2:88:26 |
| 20.86 | HueS-O1-Bar | c4:29:96:e2:46:d6 |
| 20.88 | HueS-03-Chandelier | c4:29:96:e1:ad:30 |
| 20.89 | HueS-19-Upstairs | c4:29:96:e2:53:66 |
| 20.90 | HueS-08-Library | c4:29:96:e2:d7:7a |
| 20.91 | HueS-19-Roof | c4:29:96:e2:96:ee |
| 20.92 | HueS-02-Great Room | c4:29:96:e2:22:26 |
| 20.93 | HueS-11-Kitchen | c4:29:96:e2:00:d8 |
| 20.94 | HueS-04-Dining | c4:29:96:e2:49:d0 |
| 20.95 | HueS-26-Theatre | c4:29:96:e2:db:fa |
| 20.96 | HueS-09-SunRoom | c4:29:96:e2:45:f6 |
| 20.97 | HueS-13-South Hall | c4:29:96:e1:1e:84 |
| 20.98 | HueS-26-Master2 | c4:29:96:e2:a4:b0 |
| 20.99 | HueS-05-Ground FX | c4:29:96:e2:49:e0 |

---

## LG TV Reference
| Location | Model | Year | Size | Type | OUI |
|---|---|---|---|---|---|
| Theatre (Bar) | OLED83C5PUA | 2025 | 83" | C5 evo AI | LG Electronics |
| Master Cinema | OLED77C5PUA | 2025 | 77" | C5 evo AI | LG Electronics |
| Down Guest | OLED48C5PUA | 2025 | 48" | C5 evo AI | Arcadyan (WiFi) |
| Cabana | LG C5 | 2025 | TBD | C5 evo AI | Arcadyan (WiFi) |
| Sunroom | OLED83G2PUA | 2022 | 83" | G2 Gallery | LG Electronics |
| 2nd Floor Guest | OLED65G1PUA | 2021 | 65" | G1 Gallery | LG Electronics |

## Status (2026-02-09)
- **86 fixed IP reservations created** via UniFi REST API
- **21 Hue Sync Boxes** already had fixed IPs (20.79-20.99)
- **SNS-Hers** assigned to 0.105 (0.108 used by AP-Pool)
- Devices will pick up new IPs on next DHCP renewal or reboot

## Issues / TODO
1. AP-Library (.0.81), AP-Bar (.0.32), AP-Pool (.0.108) on wrong subnet — cosmetic, still reachable
2. HueB-07-Entrata is `not_home` — check if offline or decommissioned
3. ~~Hue Sync Boxes need discovery~~ DONE — 21 found at 20.79-20.99
4. FX-Mac and Show-Mac MACs needed when online
5. 2nd Floor Guest TV MAC needed when connected
6. Add LG webOS integration for all TVs (currently Cast-only)
7. Reboot/renew devices to pick up new IPs (especially Sonos, touch panels, Hue bridges)
