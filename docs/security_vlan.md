# Security VLAN 4 — Full Inventory (2026-02-13)

## IP Scheme
| Range | Purpose | Count |
|---|---|---|
| .1 | Gateway interface | 1 |
| .7 | SEC-NVR (UNVR Pro) | 1 |
| .8 | SEC-AI-Key | 1 |
| .10-.11 | Access Hubs | 2 |
| .20-.26 | Access Readers/Intercoms | 7 |
| .40-.43 | Cameras — Entry/Front | 4 |
| .50-.56 | Cameras — Garden/Perimeter | 7 |
| .60-.67 | Cameras — Interior | 8 |
| .70-.75 | Cameras — Outdoor Structures | 6 |
| .80-.83 | Cameras — Roof | 4 |

## Access Devices (9 total)

### Access Hubs
| Name | Model | Current IP | Target IP | MAC |
|---|---|---|---|---|
| AXS-Gate-Hub | UA-GATE (Hub Gate) | .46 | .10 | 1c:6a:1b:5b:79:38 |
| AXS-Door-Hub | EAH 8 (Hub Enterprise) | .229 | .11 | 1c:6a:1b:3e:9c:15 |

### Access Readers/Intercoms
| Name | Model | Current IP | Target IP | MAC |
|---|---|---|---|---|
| AXS-Gate | G3 Intercom | .119 | .20 | 84:78:48:32:c7:80 |
| AXS-Entrata | G3 Intercom | .194 | .21 | 1c:0b:8b:cc:85:1e |
| AXS-NorthPorta | G3 Intercom | .48 | .22 | 1c:0b:8b:cc:8b:fa |
| AXS-MotorCourt | G3 Reader Pro | .94 | .23 | 1c:0b:8b:d0:db:64 |
| AXS-PlazaGate | G3 Reader Pro | .115 | .24 | 1c:0b:8b:d0:e5:f2 |
| AXS-GarageIn | G3 Reader Pro | .120 | .25 | 1c:0b:8b:d0:ed:00 |
| AXS-Cabana | G3 Reader Pro | .246 | .26 | 1c:0b:8b:d0:e7:fa |

### Door Assignment
- **Gate Hub** (.46→.10): Controls Villa Gate (the only working door)
- **Door Hub** (.229→.11): Controls 7 interior door strikes (was offline, user fixed 2026-02-13)
- G3 Intercoms have built-in cameras (visible in Protect)
- G3 Reader Pros have built-in cameras (visible in Protect)

## Cameras (29 pure + 7 Access-embedded = 36 total in Protect)

### Entry/Front (.40-.43)
| Name | Model | Target IP | MAC |
|---|---|---|---|
| CAM-VillaRollup | AI Pro + Enhancer | .40 | 1c:6a:1b:88:1a:a0 |
| CAM-Vestibule | AI Dome | .41 | 1c:0b:8b:92:96:47 |
| CAM-MotorCourt | AI Dome | .42 | 1c:0b:8b:92:df:93 |
| CAM-Road | AI LPR | .43 | 94:2a:6f:d0:bf:20 |

### Garden/Perimeter (.50-.56)
| Name | Model | Target IP | MAC |
|---|---|---|---|
| CAM-Garden | G6 Pro 360 | .50 | 1c:0b:8b:94:bc:ff |
| CAM-GardenDome | AI Dome | .51 | 1c:0b:8b:92:99:85 |
| CAM-Hill | AI Pro + Enhancer | .52 | 1c:6a:1b:81:e5:7a |
| CAM-NorthLawn | G6 Pro 360 | .53 | 1c:0b:8b:94:ba:e1 |
| CAM-EastLawn | G6 Pro 360 | .54 | 1c:0b:8b:94:bd:7f |
| CAM-DoggyCam | G6 Instant | .55 | 84:78:48:2a:10:ca |
| CAM-Playground | G6 PTZ | .56 | 8c:30:66:c6:7d:d1 |

### Interior (.60-.67)
| Name | Model | Target IP | MAC |
|---|---|---|---|
| CAM-Kitchen | G6 Instant | .60 | 84:78:48:2a:17:0c |
| CAM-Dining | G6 Instant | .61 | 84:78:48:2a:19:e0 |
| CAM-Bar | G6 Instant | .62 | 84:78:48:2a:18:e6 |
| CAM-SouthHall | G6 Instant | .63 | 84:78:48:2a:0c:c0 |
| CAM-UpperHall | G6 Instant | .64 | 84:78:48:2a:22:f4 |
| CAM-SunRoom | AI Theta | .65 | 28:70:4e:19:3c:1c |
| CAM-MachRoom | AI 360 | .66 | 1c:6a:1b:83:03:78 |
| CAM-Garage | AI Dome | .67 | 1c:0b:8b:92:9f:d3 |

### Outdoor Structures (.70-.75)
| Name | Model | Target IP | MAC |
|---|---|---|---|
| CAM-Veranda | G6 Pro 360 | .70 | 1c:0b:8b:94:bc:9d |
| CAM-Loggia | G6 Instant | .71 | 84:78:48:2a:1b:2e |
| CAM-Terrace | AI Dome | .72 | 1c:0b:8b:92:db:b8 |
| CAM-Pool | AI Pro + Enhancer | .73 | 28:70:4e:1f:0e:56 |
| CAM-Cabana | G6 Instant | .74 | 84:78:48:2a:0a:d8 |
| CAM-Plaza | AI Pro + Enhancer | .75 | 28:70:4e:1e:f1:29 |

### Roof (.80-.83)
| Name | Model | Target IP | MAC |
|---|---|---|---|
| CAM-RoofNorth | G6 Dome | .80 | 94:2a:6f:d0:cc:d9 |
| CAM-RoofSouth | G6 Dome | .81 | 94:2a:6f:d0:cd:02 |
| CAM-RoofEast | G6 Dome | .82 | 1c:0b:8b:f4:c1:63 |
| CAM-RoofWest | G6 Dome | .83 | 1c:0b:8b:f4:c4:d4 |

## Infrastructure
| Name | Model | IP (keep) | MAC |
|---|---|---|---|
| SEC-NVR | UNVR Pro | .7 | 0c:ea:14:32:66:01 |
| SEC-AI-Key | UP-AI-KEY-123E4B | .8 | 8c:ed:e1:12:3e:4b |

## Unavailable Cameras (5)
Upper Hall (.64), Cabana-cam (.74), Plaza (.75), Bar (.62), Playground (.56) — physical issue, not network.

## Migration Status (2026-02-13)
- **39/40 DHCP reservations pushed** (SEC-NVR is managed device, stays at .7 natively)
- **SW-Security restarted** to force DHCP renewal on all PoE devices
- **34/40 confirmed on new IPs** (all online devices migrated)
- **5 cameras offline** (were unavailable before migration): .56 Playground, .62 Bar, .64 Upper Hall, .74 Cabana, .75 Plaza
- **Gate Hub** still at .46 — likely has static IP set at device level via NVR Access controller. Needs manual fix in Access settings.
- **Test suite updated** to new IPs: 12/13 security tests passing (Gate Hub is the failure)

## Architecture Notes
- **EFG cannot run Access** — only Network app. Access runs exclusively on NVR.
- **Access ports on NVR**: 12443 (HTTPS API), 12812 (MQTT messaging)
- **Access readers use port 8080** (inform protocol). Hubs also have SSH (22).
- **HA Protect integration** doesn't expose camera IP addresses. MACs only in device registry `connections` field.
- **Template API trick**: `device_attr(device_id(entity), "connections")` to extract MACs for all cameras in one call.

## Firewall Rules (TODO — pending user action in Fortress UI)
Current: "Allow Core→SEC" with "Match Opposite" (overly permissive)
Plan:
1. Remove "Match Opposite" from "Allow Core→SEC"
2. Add "Allow HA→NVR" (192.168.1.6 → 192.168.4.7, TCP 443,7443,7441,7444)
3. Add "Allow Crestron→SEC-Cameras" (192.168.1.82-1.95 → Security, TCP 554,7441)
4. Add "Block Guest→SEC" and "Block IoT→SEC"
5. Keep "Block SEC→VLANs" as catch-all deny (last in creation order)
