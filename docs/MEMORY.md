# Villa Romanza - Key Learnings

## Home Assistant MCP Tools
- **Config Entry light groups** via MCP `ha_create_config_entry_helper` fails (2-step menu flow). **Workaround**: Use HA REST API directly with curl — POST `/api/config/config_entries/flow` (handler: "group"), then POST `{"next_step_id":"light"}` to advance menu, then POST entity config. Token in settings.local.json line 74.
- **Old-style groups** (`group.set`/`group.remove`) create `group.xxx` entities, NOT `light.xxx` entities. Don't confuse them.
- `ha_config_set_automation` works well for both creating (omit identifier) and updating (provide identifier) automations.
- Deep search (`ha_deep_search`) is invaluable for finding where entities are referenced across automations.
- **`ha_search_entities` fuzzy matching is unreliable** for similar names (e.g., "mads" matches "maids", "theatre" matches "Master Cinema"). Always use `ha_get_entity` for precise `area_id` lookups.
- **Config flows via REST API** work for adding integrations: POST `/api/config/config_entries/flow` with `{"handler":"<domain>"}`, then POST to the flow_id with required fields.

## System Constitution
- **Full document**: `memory/system_constitution.md` (v1.1) — source of truth for all system design
- **Signal Authority**: Crestron > HA > AI Agents (safety, mode); Hue/HA > Crestron > AI (lighting)
- **Modes**: NORMAL, LISTEN, WATCH, ENTERTAIN, LIVE_JAM/SHOW, INTERLUDE
- **Execution Nodes**: Mech Mac (LEA/reasoning), FX Mac (audio→NDI), Show Mac (TouchDesigner), CP4-R (authority), VRROOM (timing)
- **Safety Allowlist**: light.* (excl Master/Security), media_player.* (transport, max 70% vol), input_select.villa_mode, sensor.*
- **Agent entities**: prefix `agent_controlled_[domain]_[name]`
- **Autonomy Phases**: Manual → Assisted → Bounded → Expressive

## Villa Romanza Architecture
- **Domain layer**: `input_boolean.public_all`, `input_boolean.bedroom_suites_service_active`, `input_boolean.master_suite_service_active`
- **Global → Domain → Room** fanout pattern: Global activates domain toggles, domain toggles activate room booleans
- **Hard Rule 4**: Laundry and garage are NEVER activated by global/domain service
- **Master suite** is deliberately excluded from global service activation
- `input_boolean.service` is an orphaned toggle (referenced only by a disabled duplicate automation)
- `light.master_suite` (Hue zone, 71 bulbs) vs `light.master_suite_2` (HA light group, 5 rooms) — different entities
- There was a duplicate automation `observer_service_global_room_service_fanout_2` that competed with `observer_global_service_awareness` — now disabled

## HA Floors & Areas (2026-02-09)
- **76 areas** across 5 floors (consolidated from 97). `whole_house` is unassigned (virtual grouping).
- **Basement** (level -1): Cava Romanza, Mech Room — **ONLY these 2 rooms**
- **Ground Floor** (level 0): ~42 areas — all main living, master suite wing, Lower Guest, halls, utility
- **Upper Floor** (level 1): 12 areas — Pink/Blue suites (bed+bath+sink each), 2nd Guest Suite+bath, Upper Hall, Up Laundry, Balcony
- **Outdoor** (level 0): 23 areas — Pool, Lawn, Cabana, Veranda, Gate, Garden, etc.
- **Roof** (level 2): 1 area (Roof)
- **Naming conventions**: NO personal names in the system. Mad's Room = Pink Suite, Matthew's Room = Blue Suite, Maid's Quarters = Lower Guest Quarters.
- **"Maiden"** is an OUTDOOR lighting feature near the pool — NOT related to "Maid's". Devices assigned to Pool area.
- **Lower Guest Quarters/Bath** are GROUND FLOOR (slightly below grade), NOT basement.
- **Crestron has NO floor concept** — flat room list only. Floors are HA-only.
- **Bedroom suites** have 3 sub-areas: Bedroom, Bath, Sink/WC (except Master which has 12 sub-rooms, Lounge which has 2)
- **Renamed light groups**: `light.lower_guest_bedroom` (was maids_bedroom), `light.lower_guest_bath_lights` (was maids_bath_lights)

## Villa Romanza Network (Post-Migration 2026-02-07)
- **Core (VLAN 1)**: 192.168.0.0/23 — Sonos, Crestron, TVs, AVRs, HA-CORE, printers
- **Security (VLAN 4)**: 192.168.4.0/24 — UNVR Pro, AI Key, 36 cameras, 9 Access devices. See `memory/security_vlan.md`
- **Smart Things (VLAN 6)**: 192.168.6.0/24 — MyQ, iRobot, sprinklers
- **Guests (VLAN 7)**: 192.168.7.0/24 — Guest WiFi
- **Lighting (VLAN 20)**: 192.168.20.0/24 — 25 Hue Bridges + 21 Hue Sync Boxes
- **Gateway**: Enterprise Fortress Gateway ("VR The Mighty Fortress")
- **Fixed IP lockdown**: Core+Lighting COMPLETE (2026-02-09, 86 devices). Security VLAN COMPLETE (2026-02-13, 39/40 pushed, 34 confirmed on new IPs, 5 cameras were already offline, Gate Hub static-IP issue).
- **Core VLAN IP scheme**: 1.1-1.9 infra, 1.10-1.65 switches, 1.30-1.50 APs, 1.70 VRROOM, 1.71-1.78 TVs, 1.76-1.81 ATVs, 1.82-1.95 touch panels, 0.100-0.125 Sonos (0.105=SNS-Hers, 0.108=AP-Pool), 0.130-0.132 AVRs, 0.140-0.142 Mac minis
- **Lighting VLAN IP scheme**: 20.10-20.38 Hue bridges, 20.79-20.99 Hue Sync boxes (already assigned)
- **VRROOM**: MAC `18:9b:a5:d4:12:cb`, IP 192.168.1.70 — timing/EDID authority
- **UniFi API access**: Tools NOT discoverable via ToolSearch (lazy-loading). **Workaround**: Direct REST API with 2FA email code + CSRF token from `X-Csrf-Token` response header. PUT `/proxy/network/api/s/default/rest/user/{_id}` for reservations.
- **Switch SSH**: user `5Yr2N8fC` / pass `EZMg4pf9` (from Site > Device SSH settings). `swctrl port restart id <ports> interval <secs>` bounces any port.
- **DHCP renewal tricks**: `power-cycle` only works on PoE ports (not non-PoE devices). Switch restart (`cmd/devmgr restart`) bounces ALL ports. `swctrl port restart` via SSH is most targeted. Force-provision does NOT bounce ports.
- **Reusable script**: `/Users/mattserletic/unifi-tools/dhcp_force_renew.py` — modes: `--verify`, `--reserve-only`, `--restart-switches`, `--bounce-ports IP:PORTS`
- **mDNS reflector**: Enabled for cross-VLAN Hue bridge discovery
- **Firewall**: EFG rules processed in creation order (NOT display). RFC1918 Private rule disabled (TODO: replace with specific per-VLAN blocks)
- **"Allow Core→SEC" rule**: Required for HA (Core VLAN) to reach NVR/cameras (Security VLAN). Also covers Crestron touch panels accessing cameras.
- **NVR**: SEC-NVR at 192.168.4.7, SW-Security port 24. UniFi Protect integration restored (31/36 cameras online).
- **"Block SEC→VLANs" rule**: Recreated AFTER allow rules so it processes last. "Auto Allow Return Traffic" handles TCP return (stateful) but NOT ICMP.
- **Security VLAN IP scheme** (target): .7 NVR, .8 AI Key, .10-.11 Access Hubs, .20-.26 Access Readers, .40-.83 Cameras. Full inventory in `memory/security_vlan.md`.

## UniFi Access (2026-02-13)
- **9 devices**: 2 hubs (Gate Hub, Door Hub/EAH 8) + 7 readers (3x G3 Intercom, 4x G3 Reader Pro)
- **EFG cannot run Access** — only Network. Access controller runs exclusively on UNVR Pro (NVR).
- **Door Hub** controls 7 interior door strikes. **Gate Hub** controls Villa Gate independently.
- **Access ports**: NVR 12443 (API), 12812 (MQTT). Readers: 8080 (inform). Hubs: 22 (SSH) + 8080.
- **All 9 online** (Door Hub was offline, user fixed). 36 cameras: 31 online, 5 unavailable.
- **40 DHCP reservations** pushed via API (39 OK, NVR is managed device). SW-Security restarted → 34/40 on new IPs.
- **Gate Hub** still at .46 — likely device-level static IP via NVR Access settings. Needs manual fix.
- **Firewall tightening TODO**: Remove "Match Opposite" from Allow Core→SEC, add specific rules. Plan in `frolicking-snuggling-emerson.md`.
- **58 system tests** (57 passing, 1 xfail: Gate Hub). TestAccessDevices uses new reserved IPs.

## LG TV Inventory (2026-02-08)
- **TV-Theatre** (.72): OLED83C5PUA 83" C5 2025, MAC `58:96:0a:40:cc:9f`
- **TV-MasterCinema** (.71): OLED77C5PUA 77" C5 2025, MAC `60:75:6c:32:c3:f2`
- **TV-DownGuest** (.73): OLED48C5PUA 48" C5 2025, MAC `1c:f4:3f:0d:80:c4` (Arcadyan WiFi)
- **TV-Cabana** (.78): LG C5 2025, MAC `08:27:a8:23:50:62` (Arcadyan WiFi)
- **TV-Sunroom** (.74): OLED83G2PUA 83" G2 2022, MAC `b0:37:95:16:fd:f0`
- **TV-2ndGuest** (.75, deferred): OLED65G1PUA 65" G1 2021, MAC TBD
- Modern C5s use Arcadyan WiFi modules (OUI shows Arcadyan, not LG)
- "Theatre" = bar theatre, "Master Cinema" = master suite cinema
- **webOS integration**: TV-Theatre paired (entry `01KHDS0YENCKFCRNCBX53XX6GK`). Entity: `media_player.tv_theatre`. SIMPLINK must be ON for CEC chain. Other TVs NOT yet paired.
- **Mystery 42" C5** (OLED42C5PUA) discovered — not in original inventory
- **webOS API init delay**: After WoL wake, need 5s delay before sending commands — API not ready immediately

## Apple TV Inventory (2026-02-09)
- **ATV-MasterBedroom** (.76): Apple TV 4K gen 3
- **ATV-Theatre** (.77): Apple TV 4K gen 3 (was ATV-Bar, renamed 2026-02-14)
- **ATV-Bar2** (.79): Apple TV 4K gen 3 (second Bar-area ATV)
- **ATV-Sunroom** (.80): Apple TV 4K gen 2
- **ATV-Cabana** (.81): Apple TV 4K gen 2
- **ATV-Theatre paired** (2026-02-14): entry `01KHDSAJRMVMV650HGZWWK8927`, entities: `media_player.atv_theatre`, `remote.atv_theatre`. 3-step PIN pairing (AirPlay, Companion, RAOP). Other ATVs NOT yet paired.

## Anthem AVR Integration (2026-02-14)
- **AVR-Theatre** (.130): MRX-740, `media_player.avr_theatre`, area: Theatre, MAC `50:1e:2d:43:a0:c0`, entry `01KH62QPRWS1GQANQQZAKST1D0`
- **AVR-Master** (.131): MRX-540, `media_player.avr_master`, area: Master Cinema, MAC `50:1e:2d:43:93:72`, entry `01KH62QQ113DG9T40HYV8ZRYHZ`
- **AVR-Sunroom** (.132): MRX SLM — **NOT COMPATIBLE** with `anthemav` integration. Awaiting update.
- AVR IPs are at 192.168.**0**.x (not 1.x) — same Core VLAN /23 but different octet
- **Power control asymmetry**: `Z1POW1` (ON) works via serial/HA. `Z1POW0` (OFF) **silently ignored** over IP/serial. Power OFF only via CEC chain.
- **CEC power chain**: TV `system/turnOff` → HSB → VRROOM → eARC OUT → Anthem standby. Requires SIMPLINK ON (TV) + CEC Control ON + CEC Power-Off Control ON (Anthem).
- **Boot race condition**: After power-on, AVR sends status dump with defaults (TV Music, -35 dB). Commands sent during this window are overwritten. Fix: `continue_on_error: true` + retry loops in scripts.
- **Anthem settings**: Connected Standby ON, Standby HDMI Bypass: Last Used, HDMI Audio to TV OFF, Power-On Input: Last Used

## Xbox Integration (2026-02-14)
- **XBX-Theatre**: Xbox Series X, entry `01KHDSPZEXPZDFF7BFNM8ZBF1C`, account: msruns
- **Entities**: `media_player.xbx_theatre`, `remote.xbx_theatre`, storage sensors. Area: Theatre.
- **Cloud-based**: Via Microsoft account OAuth (Nabu Casa link). Power on/off (sleep mode), app launch, media control.
- **VRROOM Port 1 / RX1**: Xbox input

## Theatre AV Scripts (2026-02-14)
- **`script.watch_theatre`**: WoL TV + AVR on + VRROOM route + Rest scene (parallel) → wait TV → 5s webOS init → configure TV (HDMI 1, external_arc) → wait AVR → retry source (Cinema, max 5) → retry volume (0.3, max 3) → enable HSB sync. Has `source` field (0-3). ~20s runtime.
- **`script.theatre_off`**: Disable sync → `webostv.command` `system/turnOff` (NOT `media_player.turn_off` which goes to Gallery mode) → CEC cascades standby to Anthem → lights off. ~7s runtime.
- **Key pattern**: `continue_on_error: true` on all TV/AVR service calls prevents webOS API errors from aborting entire script. `repeat/while` with `state_attr()` checks for deterministic AVR config.
- **`button.wol_tv_theatre`**: Wake on LAN (entry `01KHF5NPFJZ890VEW185876CFH`). Built-in webOS WoL returns 500 error — separate `wake_on_lan` integration needed.
- **TV Gallery Mode**: `media_player.turn_off` sends LG C5 to Gallery+ screensaver, NOT standby. Must use `webostv.command` with `system/turnOff`.

## Crestron Integration (2026-02-07)
- **CP4-R**: 192.168.1.2 (Core VLAN), Crestron Home OS v4.009.0110, VRROOM device, 14 touch panels
- **SSH**: `VillaAdmin@192.168.1.2` / `Romanza5150!!` (use sshpass -f with password file, NOT inline)
- **REST API**: Token `TLkVgJbnF8bk`, auth via GET `/cws/api/login` → returns `authkey`; only `/rooms` endpoint useful, no device management
- **HACS**: Installed on HA Green (192.168.1.6) via SSH method
- **ha-crestron-home** (HACS custom repo): 0 entities — CP4-R has no native lighting loads
- **Crestron MCP server**: `/Users/mattserletic/crestron-mcp/` — session drops between calls (bug in global _session state)
- **CPLLC**: Full site license (all 103 products). HA Platform extension installed, licensed (key: `0536-10B7-4D61-E44B-D391-998A-72F6`), v4.000.0672
  - 53 HA entities synced (all with "crestron" label)
  - `CPLLC`/`CPLLC2` console commands return empty (debug mode via `CPLLC debug on` triggers log dump)
  - `ASSOCDEV` command exists but no working syntax found for gateway sub-devices
  - **Sub-devices are RUNTIME ONLY** — not in DeviceManifest.cfg until manually paired via Setup app
  - **No programmatic pairing API** — must use Crestron Home Setup app (XPanel or touch panel)
- **HA areas fixed**: 11 renamed + 7 created (incl Pink Bath, His WC, Her WC) to match Crestron room names
- **Light group splitting** (2026-02-08): 11 new HA light groups created to split combined Hue rooms into bedroom/bath/WC. Old combined entities de-labeled. SSH port 22 closed on HA Green — used REST API curl workaround instead.
- **Crestron plan**: `/Users/mattserletic/.claude/plans/frolicking-skipping-dragonfly.md`
- **Crestron "Bar" room has both Bar AND Theatre lights** — needs splitting in Setup app to create separate "Theatre" room
- **Crestron entities with ugly names**: `light.bar_bar_light_theatre` (moved to Theatre area), `light.bar_bar_light_bar` (in Bar area) — both platform: crestron_home
- **47 Crestron touch panel devices** have raw entity_id format names — need friendly names
- **Crestron rooms**: 61 total (includes Theatre, Master Cinema, Master Bedroom, Lower Guest Quarters/Bath already added)
- **Rooms still to add**: Pink Suite (WC), Blue Suite (WC) — bedrooms/baths already exist
- **Anthem drivers on Crestron**: Installation attempted but Setup app froze ("system initializing"). CP4-R rebooted. Zero media zone devices — drivers need re-pairing via Setup app.
- **No HDFury/VRROOM Crestron driver** — CPLLC catalog has nothing. Use HA as control plane.

## Agent Control Scaffolding (2026-02-08)
- **`input_select.villa_mode`**: 7 modes (NORMAL, LISTEN, WATCH, ENTERTAIN, LIVE_JAM, SHOW, INTERLUDE), initial: NORMAL
- **Agent-controlled entities** (all labeled `agent_controlled`, purple):
  - `input_boolean.agent_controlled_lighting_enable` (off) — gate for AI lighting
  - `input_boolean.agent_controlled_media_enable` (off) — gate for AI media
  - `input_boolean.agent_controlled_visual_enable` (off) — gate for AI visuals
  - `input_number.agent_controlled_lighting_intensity` (0-1, step 0.01)
  - `input_number.agent_controlled_visual_bias` (0-1, step 0.01)
  - `input_text.agent_controlled_visual_stinger` — stinger ID
  - `input_text.agent_controlled_thematic_pack` — pack ID
  - `input_select.agent_controlled_autonomy_phase` (manual/assisted/bounded/expressive)
- **Automations created**:
  - `automation.safety_mech_offline_recovery` — disables agent booleans when Mech Mac (device_tracker.matts_mac_mini) goes offline (Section 15)
  - `automation.observer_villa_mode_change` — logs mode transitions
- **Mech Mac**: `device_tracker.matts_mac_mini` (state: home)
- **MCP servers**: home-assistant (connected), crestron (connected), unifi-network-mcp (connected, user-level scope)
- **UniFi MCP**: `uvx --python 3.13 unifi-network-mcp`, host 192.168.1.1, port 443, user mattserletic@mac.com. Lazy-loads 67 tools via 3 meta-tools. All mutating tools require confirm=true.
- **Hue MCP** (rmrfslashbin/hue-mcp): Go-based, multi-bridge, early-dev. Needs physical button press per bridge — impractical for 29 bridges. HA already controls all Hue lights.

## HDFury VRROOM Integration (2026-02-14)
- **Device**: HDFury VRROOM-11, FW 0.62, HW rev 3, serial 0005030723004811, MAC `18:9b:a5:d4:12:cb`, IP 192.168.1.70
- **HA integration**: `hdfury` handler, config entry `01KH69R2PV6MC0HVYPP2BQ7EXE`, state: loaded
- **Control**: HA `select.hdfury_vrroom_11_port_select_tx0` works reliably. Direct HTTP `/cmd?` API returns OK but does NOT change values.
- **REST API**: `http://192.168.1.70/ssi/infopage.ssi` (status JSON), `/ssi/edidpage.ssi` (EDID config), `/ssi/cecpage.ssi` (CEC/eARC), `/ssi/confpage.ssi` (config)
- **VRROOM Input Map** (visually confirmed 2026-02-14):
  - Port 0 / RX0: Show Mini (TouchDesigner) — `device_tracker.show_mini`
  - Port 1 / RX1: Xbox
  - Port 2 / RX2: FX Mini (audio→NDI) — `device_tracker.fx_mini`
  - Port 3 / RX3: Apple TV (ATV-Bar, .77)
  - Port 4: Splitter mode (TX0 mirrors TX1)
- **Signal Chain**: Sources → VRROOM → TX0 → HSB Theatre HDMI1 → TV-Theatre HDMI 1; TX1 → mux → 3x 8ch splitters → 18 HSBs + Library TV; eARC Out → Anthem eARC
- **eARC OUT is a passthrough relay** — routes TV eARC → Anthem. TV MUST have eARC On + Digital Sound Out: Pass Through. Audio chain: Source → VRROOM → HSB → TV → eARC return → VRROOM → eARC OUT → Anthem.
- **`earctxmode: 1`** = TV eARC → eARC OUT (correct for passthrough). `earctxmode: 0` does NOT route input audio to eARC OUT.
- **Reboot command**: `curl http://192.168.1.70/cmd?reboot=1` — works via HTTP API. Resets HDMI handshakes; TV eARC may revert to 2ch PCM after.
- **EDID audio mode**: `audiotx0` (copies TV's 2ch PCM caps) — should be `allaudio` for multichannel
- **4K120**: EDID has FRL5 enabled but sources output 4K60 (macOS display settings?)
- **No Crestron driver available** — CPLLC has no HDFury driver. HA is the control plane.
- **NVR restored** (2026-02-11): SEC-NVR at 192.168.4.7, 10 GbE direct to Fortress. Was unreachable due to "Block SEC→VLANs" firewall rule killing return traffic. **Fix**: "Match Opposite" on "Allow Core→SEC" rule makes it bidirectional. 31/36 cameras online, 5 unavailable (Upper Hall, Cabana, Plaza, Bar, Playground). All 36 cameras assigned to HA areas.

## Hue Sync Boxes (2026-02-11)
- **21 HSB2 (8K) units** on Lighting VLAN (.79-.99), WiFi via "Hue-Sync" SSID. 21 paired in HA. 1 remaining: Sunroom (.96, deferred).
- **Integration**: `mvdwetering/huesyncbox` (HACS). Entity pattern: `select.{name}_sync_mode`, ~15 entities/box.
- **Pairing**: zeroconf discovery → advance `zeroconf_confirm` → `link` step (press button 3s) → advance `finish` step. Stale flows (>5 min) need HA restart.
- **Pending**: Studio (.9→.100) and Showtime (.147→.87) DHCP reservations — API rate-limited.

## Sonos (2026-02-09)
- **All 27 speakers are wired Ethernet** (confirmed via `/status/ifconfig` API on port 1400). Zero WiFi.
- **4 stale-IP master speakers** need DHCP reservations + power cycle: SNS-MasterRear (.108), SNS-MasterBedL (.126), SNS-MasterBedR (.127), SNS-MasterSub (.128). Script updated but API was rate-limited (429). Run `python3 dhcp_force_renew.py --reserve-only` with 2FA when cooldown clears, then manual power-cycle.
- **Sonos reboot API** returns 403 on all speakers. No SOAP reboot action. Manual power-cycle is only option.
- **SNS-Porch** (MAC 80:4a:f2:a8:42:a3) is offline — needs factory reset.
- **Theatre Hue lights** (11 devices) now assigned to Theatre area in HA.
