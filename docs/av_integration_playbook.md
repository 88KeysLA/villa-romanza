# AV Room Integration Playbook

Lessons learned from Theatre AV integration (2026-02-14). Use as a step-by-step template for Master Cinema and future rooms.

---

## Pre-Integration Checklist

Before starting, inventory the room's AV chain and verify:

| Item | Theatre (done) | Master Cinema (done) |
|---|---|---|
| **TV** | TV-Theatre, 192.168.1.72, LG C5 83" | TV-MasterCinema, 192.168.1.71, LG C5 77" |
| **AVR** | AVR-Theatre, 192.168.0.130, MRX-740 | AVR-Master, 192.168.0.131, MRX-540 |
| **Apple TV** | ATV-Theatre, 192.168.1.77 | ATV-MasterCinema, 192.168.1.76 |
| **Hue Sync Box** | HSB Theatre (192.168.20.92) | HSB Master2 |
| **VRROOM/switcher** | VRROOM 192.168.1.70 (shared) | None — direct HDMI |
| **Sonos Ports** | Theatre In/Out | MasterCinemaIn (→AVR), MasterCinemaOut (AVR→Sonos) |
| **Sonos Bedroom** | N/A | 5 speakers: Bed, Rear, Entry, His, Hers |
| **Hue lights** | 10 lights, Theatre area | 8 lights, Master Cinema area |
| **Xbox / other sources** | XBX-Theatre (cloud) | N/A |

### Network prerequisites
- All devices must have **fixed DHCP reservations** (use `dhcp_force_renew.py`)
- All devices must be **pingable** from HA (192.168.1.6)
- Cross-VLAN devices (cameras, NVR) require firewall allow rules

---

## Step 1 — Anthem AVR Integration

**Already done for both rooms.** AVR-Theatre (MRX-740) and AVR-Master (MRX-540) are both integrated via `anthemav`.

### Key entities
- `media_player.avr_theatre` / `media_player.avr_master`

### AVR configuration (do via AVR web UI at `http://<avr-ip>`)
- **Connected Standby**: ON (required for network wake)
- **Standby HDMI Bypass**: Last Used
- **HDMI Audio to TV**: OFF (audio stays on AVR speakers)
- **CEC Control**: ON
- **CEC Power-Off Control**: ON (allows TV power-off to cascade standby to AVR)
- **Power-On Input**: Last Used
- **Power-On Volume**: Set a safe default (e.g., -35 dB)

### Critical gotchas
1. **Power OFF does not work via HA.** `Z1POW0` is silently ignored over IP/serial. Power OFF only works via **CEC chain** (TV sends standby to AVR through HDMI).
2. **Boot race condition.** After power-on, the AVR sends a status dump with defaults (TV Music source, -35 dB volume). Any commands sent during this window (~5-8 seconds) get overwritten. **Fix**: Use `repeat/while` retry loops that check `state_attr()` until the actual value matches.
3. **Source names.** Check `state_attr('media_player.avr_master', 'source_list')` for exact source names. Theatre uses "Cinema". Master may differ.

---

## Step 2 — LG webOS TV Integration

### Pairing process
1. **TV must be ON and showing the home screen** (not standby, not an app)
2. Start config flow via HA REST API:
   ```bash
   # Get HA token from settings.local.json line 74
   TOKEN="<ha_token>"
   HA="http://192.168.1.6:8123"

   # Step 1: Initiate flow
   FLOW=$(curl -s -X POST "$HA/api/config/config_entries/flow" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"handler":"webostv"}')
   echo "$FLOW"  # Note the flow_id

   # Step 2: Submit TV IP
   FLOW_ID="<from above>"
   curl -s -X POST "$HA/api/config/config_entries/flow/$FLOW_ID" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"host":"192.168.1.71"}'
   # TV will show a pairing prompt — user must ACCEPT on TV

   # Step 3: Confirm pairing
   curl -s -X POST "$HA/api/config/config_entries/flow/$FLOW_ID" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{}'
   ```
3. Alternatively: Use `ha_config_info` to check if webOS auto-discovered the TV, then just confirm the flow.

### Post-pairing setup
- **Rename entity**: `media_player.lg_webos_tv_oled77c5pua` → `media_player.tv_master_cinema`
- **Assign area**: Master Cinema
- **Set up Wake-on-LAN**: The built-in webOS WoL returns 500 errors on C5 2025 TVs. Create a separate `wake_on_lan` integration entry:
  ```bash
  curl -s -X POST "$HA/api/config/config_entries/flow" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"handler":"wake_on_lan"}'
  # Then submit: {"mac":"60:75:6c:32:c3:f2", "name":"WoL TV-MasterCinema", "broadcast_address":"192.168.1.255", "broadcast_port":9}
  ```

### Critical gotchas
1. **`media_player.turn_off` = Gallery Mode, NOT standby.** LG C5 2025 TVs go to Gallery+ screensaver. To actually turn off the TV: `webostv.command` with `system/turnOff`.
2. **webOS API not ready for ~5 seconds after WoL wake.** Service calls made immediately after the TV reports "on" will fail. Always add a 5s delay after `wait_for_trigger` on the TV state.
3. **SIMPLINK must be ON** in TV settings for CEC chain to work (TV off → AVR standby).
4. **HDMI input names**: Check what the TV calls them. Theatre uses "HDMI 1". Master Cinema may differ.
5. **Sound output**: Must be set to `external_arc` for eARC audio to reach the AVR. Use `webostv.select_sound_output` with `sound_output: external_arc`.

---

## Step 3 — Apple TV Integration

### Pairing process
1. **Apple TV must be ON and visible on the TV screen** (need to see the PIN)
2. Start config flow:
   ```bash
   curl -s -X POST "$HA/api/config/config_entries/flow" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"handler":"apple_tv"}'
   # Submit device IP, then follow 3-step PIN pairing
   ```
3. **Three PIN prompts** (AirPlay, Companion, RAOP) — each shows a 4-digit PIN on the TV screen that must be entered in the HA flow.

### Post-pairing setup
- **Rename entities**: `media_player.atv_*`, `remote.atv_*` to match room name
- **Assign area**: Master Cinema

### Critical gotchas
1. Pairing **requires the TV to be displaying the Apple TV UI** to see PINs
2. If the TV is off or on a different input, you can't complete pairing

---

## Step 4 — Xbox Integration (if applicable)

- **Cloud-based** via Microsoft account OAuth through Nabu Casa
- Start flow with handler `xbox`, follow Microsoft login link
- Gives: power on/off (sleep mode), app launch, media control
- **No physical pairing needed** — all via cloud

---

## Step 5 — Hue Sync Box

HSBs are already paired via `huesyncbox` HACS integration. Key entities:
- `switch.<room>_light_sync` — enable/disable light sync
- `select.<room>_sync_mode` — video/music/game mode
- `select.<room>_hdmi_input` — which HDMI input to sync from

### Gotcha
- Entertainment area must be configured in the **Hue app** (not HA) — it spans up to 5 Hue bridges per entertainment zone
- HSB audio mode should be "passthrough" for multichannel audio to reach AVR

---

## Step 6 — Area Assignments

After all integrations, move every Theatre/Cinema device to the correct HA area:
```
ha_update_device(device_id, area_id="<room_area>")
ha_rename_entity(entity_id, name="<friendly_name>")
```

Entity naming convention:
- `media_player.tv_<room>` — webOS TV
- `media_player.avr_<room>` — Anthem AVR
- `media_player.atv_<room>` — Apple TV
- `media_player.xbx_<room>` — Xbox
- `media_player.<room>_in` / `<room>_out` — Sonos Ports
- `button.wol_tv_<room>` — Wake on LAN
- `switch.<room>_light_sync` — Hue Sync Box

---

## Step 7 — Create Power-On Script

Template based on working `script.watch_theatre`:

```yaml
alias: "Watch <Room>"
description: >
  Powers on all <Room> AV equipment with verified sequencing.
  Retry loops for AVR, continue_on_error for TV commands.
icon: mdi:movie-open
mode: single
fields:
  source:
    name: Source
    description: "Input source (adjust per room)"
    default: "apple_tv"
    selector:
      select:
        options:
          - {value: "apple_tv", label: "Apple TV"}
          # Add room-specific sources
sequence:
  - alias: "Phase 1 — Parallel power on"
    parallel:
      - action: button.press
        target:
          entity_id: button.wol_tv_<room>
      - sequence:
          - delay: {seconds: 2}
          - action: media_player.turn_on
            target:
              entity_id: media_player.avr_<room>
      # VRROOM routing (Theatre only — Master Cinema may be direct HDMI)
      # - action: select.select_option
      #   target:
      #     entity_id: select.hdfury_vrroom_11_port_select_tx0
      #   data:
      #     option: "{{ source_port }}"
      - action: scene.turn_on
        target:
          entity_id: scene.<room>_rest  # or appropriate scene

  - alias: "Phase 2 — Wait for TV online (max 30s)"
    wait_for_trigger:
      - trigger: state
        entity_id: media_player.tv_<room>
        to: "on"
    timeout: {seconds: 30}
    continue_on_timeout: true

  - alias: "Phase 2b — webOS API init delay"
    delay: {seconds: 5}

  - alias: "Phase 3 — Configure TV"
    if:
      - condition: state
        entity_id: media_player.tv_<room>
        state: "on"
    then:
      - action: media_player.select_source
        target:
          entity_id: media_player.tv_<room>
        data:
          source: "HDMI 1"  # verify per room
        continue_on_error: true
      - delay: {seconds: 2}
      - action: webostv.select_sound_output
        target:
          entity_id: media_player.tv_<room>
        data:
          sound_output: external_arc
        continue_on_error: true

  - alias: "Phase 4 — Wait for AVR"
    choose:
      - conditions:
          - condition: state
            entity_id: media_player.avr_<room>
            state: "on"
        sequence:
          - delay: {seconds: 5}
    default:
      - wait_for_trigger:
          - trigger: state
            entity_id: media_player.avr_<room>
            to: "on"
        timeout: {seconds: 45}
        continue_on_timeout: true
      - delay: {seconds: 8}

  - alias: "Phase 5 — Set AVR source (retry max 5)"
    repeat:
      while:
        - condition: template
          value_template: >
            {{ repeat.index <= 5 and
               state_attr('media_player.avr_<room>', 'source') != '<SOURCE>' }}
      sequence:
        - action: media_player.select_source
          target:
            entity_id: media_player.avr_<room>
          data:
            source: "<SOURCE>"  # check source_list
          continue_on_error: true
        - delay: {seconds: 3}

  - alias: "Phase 5b — Set AVR volume (retry max 3)"
    repeat:
      while:
        - condition: template
          value_template: >
            {{ repeat.index <= 3 and
               ((state_attr('media_player.avr_<room>', 'volume_level') | float(0)) - 0.3) | abs > 0.02 }}
      sequence:
        - action: media_player.volume_set
          target:
            entity_id: media_player.avr_<room>
          data:
            volume_level: 0.3
          continue_on_error: true
        - delay: {seconds: 2}

  - alias: "Phase 6 — Enable light sync"
    action: switch.turn_on
    target:
      entity_id: switch.<room>_light_sync
```

### Key patterns that prevent failures
- **`continue_on_error: true`** on every TV and AVR service call — prevents webOS API errors from aborting the script
- **`repeat/while` with `state_attr()` checks** — the AVR's boot status dump overwrites commands; retries until the actual value matches
- **`wait_for_trigger` with `continue_on_timeout`** — don't hang forever if a device doesn't come online
- **5s webOS init delay** — API isn't ready immediately after WoL wake reports "on"
- **`choose` for AVR wait** — different timing for already-on vs cold-boot scenarios

---

## Step 8 — Create Power-Off Script

Template based on working `script.theatre_off`:

```yaml
alias: "<Room> Off"
description: >
  Powers off all <Room> AV equipment. Uses webOS system/turnOff
  (not media_player.turn_off which goes to Gallery mode).
  CEC cascades standby to Anthem.
icon: mdi:power-off
mode: single
sequence:
  - alias: "Phase 1 — Parallel cleanup"
    parallel:
      - alias: "Disable sync"
        action: switch.turn_off
        target:
          entity_id: switch.<room>_light_sync
      # If room has Sonos bedroom group, unjoin here:
      # - action: media_player.unjoin
      #   target:
      #     entity_id: media_player.<speaker1>, media_player.<speaker2>, ...
      # - action: media_player.turn_off
      #   target:
      #     entity_id: media_player.avr_<room>_zone2
  - delay: {seconds: 1}
  - alias: "Power off TV (real shutdown)"
    action: webostv.command
    target:
      entity_id: media_player.tv_<room>
    data:
      command: "system/turnOff"
  - delay: {seconds: 5}
  - alias: "AVR off (CEC fallback)"
    if:
      - condition: state
        entity_id: media_player.avr_<room>
        state: "on"
    then:
      - action: media_player.turn_off
        target:
          entity_id: media_player.avr_<room>
        continue_on_error: true
  - delay: {seconds: 2}
  - alias: "Turn off lights"
    action: light.turn_off
    target:
      entity_id: light.<room>
```

### Why this works
- `webostv.command system/turnOff` = real standby (not Gallery mode)
- CEC chain: TV off → HSB → HDMI → AVR standby (if CEC Power-Off Control is ON in AVR settings)
- **AVR fallback**: CEC cascade is unreliable (especially without VRROOM in the path). After 5s, if AVR is still on, explicitly turn it off via `media_player.turn_off`. Tested: `Z1POW0` works via the `anthemav` integration even though raw serial ignores it.
- Lights go off last so you're not in the dark while the system shuts down
- **Sonos unjoin in Phase 1 (parallel)**: Runs concurrently with sync disable. Speakers return to standalone mode.
- **Zone 2 off in Phase 1**: Stops signal to Sonos Port before TV shutdown

---

## Step 9 — Sonos Bedroom Audio Extension

For rooms with Anthem AVRs that have preamp/Zone 2 outputs, Sonos Ports can distribute audio to bedroom speakers. This extends the cinema experience to adjacent rooms.

### Physical wiring
```
AVR Zone 2 / Preamp Out → Sonos Port (Line-in) → Sonos Group → Bedroom Speakers
```

**Critical**: The Sonos Port receiving AVR output uses its **Line-in** jack. The other Port (if present) sends audio **to** the AVR analog input. Don't confuse them.

### Entity naming
- `media_player.<room>_in` — Sonos Port that sends audio INTO the AVR (Sonos→AVR, line-out)
- `media_player.<room>_out` — Sonos Port that receives audio FROM the AVR (AVR→Sonos, line-in)

### Setup procedure

1. **Identify the correct Sonos Port**: Find which Port has the AVR preamp cable connected to its Line-in. Play audio on the AVR, then select Line-in source on each Port candidate. The one that passes audio is the right one.

2. **Enable AVR Zone 2**: The AVR's preamp/Zone 2 output must be ON for signal to flow:
   ```yaml
   action: media_player.turn_on
     target:
       entity_id: media_player.avr_<room>_zone2
   action: media_player.select_source
     target:
       entity_id: media_player.avr_<room>_zone2
     data:
       source: "<same as main zone>"
   action: media_player.volume_set
     target:
       entity_id: media_player.avr_<room>_zone2
     data:
       volume_level: 0.3
   ```

3. **Create Sonos group**: Join bedroom speakers to the Port as group leader:
   ```yaml
   # Set Port to Line-in source
   action: media_player.select_source
     target:
       entity_id: media_player.<room>_out
     data:
       source: "Line-in"
   # Join speakers
   action: media_player.join
     target:
       entity_id: media_player.<room>_out
     data:
       group_members:
         - media_player.speaker1
         - media_player.speaker2
   # IMPORTANT: Group starts paused — must explicitly play
   action: media_player.media_play
     target:
       entity_id: media_player.<room>_out
   ```

4. **Set individual volumes**: Each speaker has independent volume within the group:
   ```yaml
   action: media_player.volume_set
     target:
       entity_id: media_player.speaker1
     data:
       volume_level: 0.22
   ```

### Gotchas

1. **Group starts paused.** After `media_player.join`, the group state is "paused". Must send `media_player.media_play` to the group leader to start audio flow.
2. **AVR mute kills preamp output.** When the AVR main zone is muted, the preamp/Zone 2 output is also muted — no signal reaches the Sonos Port.
3. **Speakers can drop from groups.** When joining new members or adjusting volumes, existing group members may silently drop. Always verify `group_members` attribute after changes.
4. **Port name confusion.** Physical wiring determines which Port is "in" vs "out". Use the test-and-play method to identify the correct one. Rename entities if they're backwards.
5. **Sonos favorites for testing.** Use `browse_media` to discover favorites: `media_content_type: "favorite_item_id"`, `media_content_id: "FV:2/<n>"`. Useful for testing individual speakers before grouping.

### Master Cinema preset (tuned 2026-02-15)

| Speaker | Entity | Volume | Notes |
|---|---|---|---|
| AVR Main Zone | `media_player.avr_master` | 30% (script) | Script sets 30%, user tunes during listening |
| AVR Zone 2 | `media_player.avr_master_zone2` | 30% | Source: "Apple TV" |
| Master Bed | `media_player.master_bed` | 22% | Era 300 stereo pair |
| Master Entry | `media_player.master_entry` | 23% | |
| His | `media_player.his` | 19% | |
| Hers | `media_player.hers` | 19% | |
| Master Rear | `media_player.master_rear` | 16% | Era 100 stereo pair |

---

## Step 10 — Verification Checklist

After integration, test each of these:

- [ ] `media_player.tv_<room>` can power on (WoL) and off (`system/turnOff`)
- [ ] TV input switches to correct HDMI source
- [ ] TV sound output is `external_arc`
- [ ] `media_player.avr_<room>` can power on and shows correct source
- [ ] AVR volume responds to `media_player.volume_set`
- [ ] Apple TV shows current playback state
- [ ] Power-on script completes in ~20-25s with correct final state
- [ ] Power-off script cleanly shuts down all devices (~10s)
- [ ] CEC chain or AVR fallback shuts AVR down
- [ ] Light sync activates and deactivates correctly
- [ ] Audio is multichannel (not 2ch stereo) — check AVR display
- [ ] (If Sonos) Zone 2 turns on and Sonos Port receives audio
- [ ] (If Sonos) All bedroom speakers join group and play audio
- [ ] (If Sonos) Power-off unjoins all speakers and stops Zone 2

---

## Test Results (2026-02-14)

### Theatre

| Test | Result | Notes |
|---|---|---|
| `watch_theatre` cold start | **PASS — 21s** | All off → all on |
| WoL TV-Theatre | **PASS** | TV woke in 4s from standby |
| TV source HDMI 1 (VRRoom) | **PASS** | Set via `media_player.select_source` |
| TV sound output `external_arc` | **PASS** | Set via `webostv.select_sound_output` |
| AVR source "Cinema" | **PASS** | Retry loop (max 5) set correctly |
| AVR volume 30% | **PASS** | Retry loop (max 3) set correctly |
| VRROOM port 3 (Apple TV) | **PASS** | Default source routed |
| HSB Theatre light sync | **PASS** | Activated after AVR config |
| Rest scene | **PASS** | Warm amber, 10 lights |
| `theatre_off` | **PASS — ~10s** | All devices off |
| TV `system/turnOff` | **PASS** | Real standby (not Gallery mode) |
| CEC → AVR standby | **PASS** | CEC cascaded within 2s via VRROOM eARC |
| AVR fallback (if needed) | **PASS** | `media_player.turn_off` as safety net |

### Master Cinema

| Test | Result | Notes |
|---|---|---|
| `watch_master_cinema` cold start | **PASS — ~25s** | All off → all on, incl Sonos group |
| WoL TV-MasterCinema | **PASS** | TV woke in 3s from standby |
| TV source HDMI 2 | **PASS** | HSB output on HDMI 2 |
| TV sound output `external_arc` | **PASS** | Set via `webostv.select_sound_output` |
| AVR source "Apple TV" | **PASS** | Retry loop set correctly |
| AVR volume 30% | **PASS** | Retry loop set correctly |
| HSB Master2 light sync | **PASS** | Activated after AVR config |
| Evening scene | **PASS** | Warm orange, 8 lights |
| Zone 2 on + source | **PASS** | `avr_master_zone2` on, source "Apple TV", vol 30% |
| Sonos group (5 speakers) | **PASS** | Bed 22%, Rear 16%, Entry 23%, His 19%, Hers 19% |
| Sonos audio from AVR | **PASS** | Line-in on `master_cinema_out` receives preamp signal |
| `master_cinema_off` | **PASS — ~10s** | All devices off, Sonos unjoined |
| TV `system/turnOff` | **PASS** | Real standby (not Gallery mode) |
| CEC → AVR standby | **FAIL** | CEC does NOT cascade (no VRROOM in path) |
| AVR fallback | **PASS** | `media_player.turn_off` shuts AVR down reliably |
| Sonos unjoin on off | **PASS** | All 5 speakers return to standalone |
| Zone 2 off on off | **PASS** | Stops preamp signal to Sonos Port |

### Key Findings

1. **CEC cascade works in Theatre** (TV → HSB → VRROOM eARC OUT → Anthem) but **not in Master Cinema** (TV → HSB → TV eARC → Anthem). The VRROOM appears to be critical for CEC relay.
2. **AVR fallback is essential.** `media_player.turn_off` via the `anthemav` integration successfully powers off the AVR, despite documentation saying `Z1POW0` is silently ignored over serial. The integration may use a different mechanism.
3. **Quick Start+ must be enabled** on LG C5 TVs for WoL to work. Without it, `system/turnOff` puts the TV in deep power-off (state: "unavailable") where the NIC is completely off. With Quick Start+, state goes to "off" (standby with NIC alive).
4. **Watch scripts are fast.** Cold start ~18-25s (longer with Sonos group), warm start ~16s. The `choose` block in Phase 4 correctly shortcuts when AVR is already on.
5. **Both rooms show 2ch PCM** on the AVR — multichannel audio is still a TODO.
6. **Sonos Port naming matters.** Physical cable determines which Port is "in" vs "out". Test by playing audio on AVR and checking which Port receives signal on Line-in. Entity names were swapped during Master Cinema setup after discovering wiring mismatch.
7. **Sonos groups start paused.** After `media_player.join`, must send `media_player.media_play` to the group leader.
8. **AVR Zone 2 required for preamp output.** Without Zone 2 ON, no signal flows from AVR preamp to Sonos Port.
9. **AVR mute kills preamp output.** Main zone mute also silences Zone 2/preamp — can't isolate bedroom speakers by muting AVR.

---

## Master Cinema — Confirmed Configuration

Verified during integration (2026-02-14):

| Item | Value |
|---|---|
| **Signal chain** | Apple TV (.76) → HSB Master2 HDMI1 → HSB OUT → TV HDMI 2 → eARC → AVR-Master (.131) |
| **TV source** | HDMI 2 (not HDMI 1 like Theatre) |
| **AVR source name** | "Apple TV" (not "Cinema" like Theatre) |
| **HSB entities** | `switch.master2_light_sync`, `select.master2_sync_mode`, `select.master2_hdmi_input` |
| **Scene** | `scene.master_theatre_evening` (warm orange, dynamic) |
| **Lights** | `light.master_theatre` (8 bulbs: Master TV, TV Floor, Lamps L/R, TV Left/Right, TV Tube, Bed Tube) |
| **No VRROOM** | Single source (Apple TV), no routing needed |
| **ATV-MasterCinema** | Renamed from ATV-MasterBedroom, dedicated to cinema |
| **CEC** | Does NOT cascade to AVR — must use explicit `media_player.turn_off` fallback |
| **Sonos Port (out)** | `media_player.master_cinema_out` — AVR preamp → Sonos (group leader, Line-in) |
| **Sonos Port (in)** | `media_player.master_cinema_in` — Sonos → AVR (line-out to analog input) |
| **AVR Zone 2** | `media_player.avr_master_zone2` — must be ON for preamp output to Sonos |
| **Sonos group** | 5 speakers: master_bed (22%), master_rear (16%), master_entry (23%), his (19%), hers (19%) |

---

## Deferred / TODO (applies to all rooms)

- **Multichannel audio**: Both rooms show 2ch PCM on AVR. Theatre likely needs VRROOM EDID `audiotx0` → `allaudio`. Master Cinema (no VRROOM) may need TV audio passthrough settings.
- **VRROOM diagnostic entities**: 11 disabled sensors to enable for audio diagnosis.
- **HSB entertainment areas**: Must be configured in Hue app (not HA) per room.
- **AVR-Sunroom**: MRX SLM not compatible with `anthemav` integration — awaiting update.
- **CEC investigation**: Why does CEC cascade work through VRROOM but not through direct HSB→TV→AVR path?
