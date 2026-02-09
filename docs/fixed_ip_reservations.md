# Villa Romanza — Complete Fixed IP Reservation List
# Created: 2026-02-08
# UniFi: Settings > Networks > [Network] > DHCP > Static IP Mapping

---

## CORE VLAN (Default Network — 192.168.0.0/23)

### Already Fixed (Infrastructure — confirm reservations exist)
| # | Name | MAC | IP | Type |
|---|---|---|---|---|
| 1 | VR The Mighty Fortress | 28:70:4e:27:97:49 | 192.168.1.1 | Gateway |
| 2 | CP4-R | c4:42:68:41:92:fb | 192.168.1.2 | Crestron Processor |
| 3 | SW-CORE | 84:78:48:60:15:b3 | 192.168.1.4 | Core Switch |
| 4 | PWR-PDU | 6c:63:f8:2e:84:c7 | 192.168.1.5 | Power Distribution |
| 5 | HA-CORE | 20:f8:3b:02:40:23 | 192.168.1.6 | Home Assistant Green |

### VRROOM + TVs (192.168.1.70-78)
| # | Name | MAC | Fixed IP | Current IP |
|---|---|---|---|---|
| 1 | VRROOM | 18:9b:a5:d4:12:cb | 192.168.1.70 | 1.70 (keep) |
| 2 | TV-MasterCinema | 60:75:6c:32:c3:f2 | 192.168.1.71 | 1.58 |
| 3 | TV-Theatre | 58:96:0a:40:cc:9f | 192.168.1.72 | DHCP |
| 4 | TV-DownGuest | 1c:f4:3f:0d:80:c4 | 192.168.1.73 | 0.127 |
| 5 | TV-Sunroom | b0:37:95:16:fd:f0 | 192.168.1.74 | 1.74 (keep) |
| 6 | TV-2ndGuest (DEFERRED) | TBD | 192.168.1.75 | not online |
| 7 | TV-Cabana | 08:27:a8:23:50:62 | 192.168.1.78 | 0.48 |

### Apple TVs (192.168.1.76-81)
| # | Name | MAC | Fixed IP | Current IP |
|---|---|---|---|---|
| 1 | ATV-MasterCinema | c4:f7:c1:2b:09:68 | 192.168.1.76 | 0.106 |
| 2 | ATV-Theatre | c0:95:6d:58:1a:5d | 192.168.1.77 | DHCP |
| 3 | ATV-DownGuest | c4:f7:c1:12:c4:ba | 192.168.1.79 | 0.154 |
| 4 | ATV-Sunroom | f0:b3:ec:32:ed:c5 | 192.168.1.80 | 0.49 |
| 5 | ATV-Cabana | f0:b3:ec:28:fa:60 | 192.168.1.81 | 0.167 |

### Crestron Touch Panels (192.168.1.82-95)
| # | Name | MAC | Fixed IP |
|---|---|---|---|
| 1 | TP-Lounge | c4:42:68:25:33:67 | 192.168.1.82 |
| 2 | TP-Entrata | c4:42:68:63:85:e0 | 192.168.1.83 |
| 3 | TP-Kitchen | c4:42:68:68:81:7a | 192.168.1.84 |
| 4 | TP-VillaMaster | c4:42:68:63:83:83 | 192.168.1.85 |
| 5 | TP-Cabana | c4:42:68:63:83:2e | 192.168.1.86 |
| 6 | TP-Garage | 00:10:7f:ef:fd:c1 | 192.168.1.87 |
| 7 | TP-VillaHis | c4:42:68:63:88:24 | 192.168.1.88 |
| 8 | TP-CavaRomanza | c4:42:68:63:82:57 | 192.168.1.89 |
| 9 | TP-Veranda | c4:42:68:63:82:ea | 192.168.1.90 |
| 10 | TP-Dining | c4:42:68:68:73:05 | 192.168.1.91 |
| 11 | TP-VillaHers | c4:42:68:63:8e:1b | 192.168.1.92 |
| 12 | TP-LaundryDown | c4:42:68:63:85:c9 | 192.168.1.93 |
| 13 | TP-NorthPorta | c4:42:68:68:73:ed | 192.168.1.94 |
| 14 | TP-Library | c4:42:68:68:b3:cc | 192.168.1.95 |

### Sonos Speakers (192.168.0.100-124)
| # | Name | MAC | Fixed IP |
|---|---|---|---|
| 1 | SNS-Library | 80:4a:f2:ae:30:5b | 192.168.0.100 |
| 2 | SNS-Lounge | c4:38:75:8d:3e:24 | 192.168.0.101 |
| 3 | SNS-Kitchen | 74:ca:60:41:8e:61 | 192.168.0.102 |
| 4 | SNS-Dining | 80:4a:f2:ae:30:61 | 192.168.0.103 |
| 5 | SNS-Entrata | 80:4a:f2:a8:43:78 | 192.168.0.104 |
| 6 | SNS-MasterEntry | 80:4a:f2:ae:c6:c1 | 192.168.0.106 |
| 7 | SNS-His | 74:ca:60:41:8f:66 | 192.168.0.107 |
| 8 | SNS-Hers | 80:4a:f2:ae:c6:b2 | 192.168.0.105 |
| 9 | SNS-BlueBedroom | 80:4a:f2:ae:c6:f1 | 192.168.0.109 |
| 10 | SNS-PinkBedroom | 80:4a:f2:ae:a2:10 | 192.168.0.110 |
| 11 | SNS-GuestUp | c4:38:75:8b:b9:83 | 192.168.0.111 |
| 12 | SNS-GuestDown | 80:4a:f2:ae:c0:be | 192.168.0.112 |
| 13 | SNS-Garage | 80:4a:f2:ae:c6:df | 192.168.0.113 |
| 14 | SNS-Wine | 80:4a:f2:a8:42:b2 | 192.168.0.114 |
| 15 | SNS-Porch | 80:4a:f2:a8:42:a3 | 192.168.0.115 |
| 16 | SNS-Lawn | 38:42:0b:26:92:5e | 192.168.0.116 |
| 17 | SNS-Picnic | 80:4a:f2:a9:7d:07 | 192.168.0.117 |
| 18 | SNS-PoolNorth | 38:42:0b:26:93:39 | 192.168.0.118 |
| 19 | SNS-PoolSouth | 74:ca:60:49:18:8a | 192.168.0.119 |
| 20 | SNS-PoolEast | 74:ca:60:e0:9a:32 | 192.168.0.120 |
| 21 | SNS-Cabana | c4:38:75:8b:7d:80 | 192.168.0.121 |
| 22 | SNS-PT-Bar | 38:42:0b:8f:11:ae | 192.168.0.122 |
| 23 | SNS-PT-SyncFeed | 38:42:0b:8f:0c:ce | 192.168.0.123 |
| 24 | SNS-PT-Sunroom | 00:1b:66:04:0a:e9 | 192.168.0.124 |
| 25 | SNS-PicnicSub | 74:ca:60:31:da:dc | 192.168.0.125 |

### AVRs (192.168.0.130-132)
| # | Name | MAC | Fixed IP |
|---|---|---|---|
| 1 | AVR-Bar (Anthem MRX 540) | 50:1e:2d:43:a0:c0 | 192.168.0.130 |
| 2 | AVR-Master (Anthem MRX 40) | 50:1e:2d:43:93:72 | 192.168.0.131 |
| 3 | AVR-Sunroom (Paradigm) | 7c:b7:7b:04:29:d1 | 192.168.0.132 |

### Mac Minis (192.168.0.140-142)
| # | Name | MAC | Fixed IP | Current IP |
|---|---|---|---|---|
| 1 | Mech-Mac (LEA) | d0:11:e5:ed:43:d4 | 192.168.0.140 | 0.105 |
| 2 | FX-Mac (DEFERRED) | TBD | 192.168.0.141 | — |
| 3 | Show-Mac (DEFERRED) | TBD | 192.168.0.142 | — |

### Other Core Devices
| # | Name | MAC | Fixed IP |
|---|---|---|---|
| 1 | PNT-Library (Printer) | 24:6a:0e:59:7c:ba | 192.168.0.150 |
| 2 | Ramonas-iMac | 78:7b:8a:aa:e4:ba | 192.168.0.151 |
| 3 | Villa Chime Plug | 58:d6:1f:1e:41:93 | 192.168.0.155 |

---

## LIGHTING VLAN 20 (192.168.20.0/24)

### Hue Bridges (192.168.20.10-38)
| # | Name | MAC | Fixed IP |
|---|---|---|---|
| 1 | HueB-01-Bar | c4:29:96:b4:14:ba | 192.168.20.10 |
| 2 | HueB-02-GreatRoom | c4:29:96:b4:22:48 | 192.168.20.11 |
| 3 | HueB-03-Chandelier | c4:29:96:b0:3d:af | 192.168.20.12 |
| 4 | HueB-04-Dining | c4:29:96:b4:12:89 | 192.168.20.13 |
| 5 | HueB-05-GroundFX | c4:29:96:b4:19:65 | 192.168.20.14 |
| 6 | HueB-06-Loggia | c4:29:96:b8:d9:4b | 192.168.20.15 |
| 7 | HueB-07-Entrata | c4:29:96:c4:23:fd | 192.168.20.16 |
| 8 | HueB-08-Library | c4:29:96:b4:23:2f | 192.168.20.17 |
| 9 | HueB-09-1stGuest | c4:29:96:b4:14:b3 | 192.168.20.18 |
| 10 | HueB-10-Upstairs | c4:29:96:b4:12:ef | 192.168.20.19 |
| 11 | HueB-11-Kitchen | c4:29:96:b0:68:ea | 192.168.20.20 |
| 12 | HueB-12-SunRoom | c4:29:96:b4:28:73 | 192.168.20.21 |
| 13 | HueB-13-SouthHall | c4:29:96:b4:15:83 | 192.168.20.22 |
| 14 | HueB-14-Master | c4:29:96:b0:3f:32 | 192.168.20.23 |
| 15 | HueB-15-Studio | c4:29:96:b4:1e:6d | 192.168.20.24 |
| 16 | HueB-17-Veranda | c4:29:96:b4:14:bc | 192.168.20.25 |
| 17 | HueB-18-WestLawn | c4:29:96:b4:1a:0e | 192.168.20.26 |
| 18 | HueB-19-Gate | c4:29:96:ba:11:b2 | 192.168.20.27 |
| 19 | HueB-19-Roof | c4:29:96:b0:3b:eb | 192.168.20.28 |
| 20 | HueB-20-Pool | c4:29:96:b4:2c:c7 | 192.168.20.29 |
| 21 | HueB-21-Lamps | c4:29:96:b4:20:0c | 192.168.20.30 |
| 22 | HueB-22-SWBed | ec:b5:fa:bb:e6:f3 | 192.168.20.31 |
| 23 | HueB-23-SEBed | ec:b5:fa:b0:8c:fa | 192.168.20.32 |
| 24 | HueB-24-2ndGuest | ec:b5:fa:9d:c0:68 | 192.168.20.33 |
| 25 | HueB-25-Theatre | c4:29:96:ba:14:84 | 192.168.20.34 |
| 26 | HueB-25-Utility | ec:b5:fa:bb:cd:32 | 192.168.20.35 |
| 27 | HueB-26-MB2 | c4:29:96:b9:a9:9f | 192.168.20.36 |
| 28 | HueB-Cabana | c4:29:96:b4:14:7a | 192.168.20.37 |
| 29 | HueB-Entrata | c4:29:96:b4:23:fd | 192.168.20.38 |

### Hue Sync Boxes (192.168.20.50-69) — DEFERRED
Hue Sync Boxes are on VLAN 20 but not visible as UniFi device_trackers.
Need to identify from Hue bridge or UniFi client list.
Reserve range 192.168.20.50-69 for ~20 sync boxes.

---

## SECURITY VLAN 4 (192.168.4.0/24)
Cameras and NVR are already managed by UniFi Protect.
| # | Name | MAC | Suggested IP |
|---|---|---|---|
| 1 | SEC-NVR | 0c:ea:14:32:66:02 | 192.168.4.2 |
| 2 | UP-AI-KEY | 8c:ed:e1:12:3e:4b | 192.168.4.3 |
Cameras: managed by Protect, typically auto-assigned.

---

## SUMMARY
| Category | Count | Ready | Deferred |
|---|---|---|---|
| VRROOM | 1 | 1 | 0 |
| TVs | 6 | 5 | 1 (2nd Guest) |
| Apple TVs | 5 | 5 | 0 |
| Touch Panels | 14 | 14 | 0 |
| Sonos | 25 | 25 | 0 |
| AVRs | 3 | 3 | 0 |
| Mac Minis | 3 | 1 | 2 (FX, Show) |
| Other Core | 3 | 3 | 0 |
| Hue Bridges | 29 | 29 | 0 |
| Hue Sync Boxes | ~20 | 0 | ~20 |
| Security | 2 | 2 | 0 |
| **TOTAL** | **~111** | **88** | **~23** |

NOTE: Switches (1.10-1.65) and APs (1.30-1.50) already have fixed IPs
managed by UniFi. 22 APs + ~20 switches = ~42 more devices already locked.
