# AV Room Integration Playbook

Lessons learned from Theatre AV integration (2026-02-14). Use as a step-by-step template for Master Cinema and future rooms.

---

## Pre-Integration Checklist

Before starting, inventory the room's AV chain and verify:

| Item | Theatre (done) | Master Cinema (TODO) |
|---|---|---|
| **TV** | TV-Theatre, 192.168.1.72, LG C5 83" | TV-MasterCinema, 192.168.1.71, LG C5 77" |
| **AVR** | AVR-Theatre, 192.168.0.130, MRX-740 | AVR-Master, 192.168.0.131, MRX-540 |
| **Apple TV** | ATV-Theatre, 192.168.1.77 | ATV-MasterBedroom, 192.168.1.76 |
| **Hue Sync Box** | HSB Theatre (192.168.20.92) | HSB Master Cinema (check IP) |
| **VRROOM/switcher** | VRROOM 192.168.1.70 (shared) | Direct HDMI? Or second VRROOM output? |
| **Sonos Ports** | Theatre In (.theatre_in), Theatre Out (.theatre_out) | Check if Master has Sonos Ports |
| **Hue lights** | 10 lights, Theatre area | Master Cinema lights, check area |
| **Xbox / other sources** | XBX-Theatre (cloud) | Any additional sources? |

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
  - alias: "Disable sync"
    action: switch.turn_off
    target:
      entity_id: switch.<room>_light_sync
  - delay: {seconds: 1}
  - alias: "Power off TV (real shutdown → CEC standby to AVR)"
    action: webostv.command
    target:
      entity_id: media_player.tv_<room>
    data:
      command: "system/turnOff"
  - delay: {seconds: 5}
  - alias: "Turn off lights"
    action: light.turn_off
    target:
      entity_id: light.<room>
```

### Why this works
- `webostv.command system/turnOff` = real standby (not Gallery mode)
- CEC chain: TV off → HSB → HDMI → AVR standby (if CEC Power-Off Control is ON in AVR settings)
- No need to explicitly turn off AVR — CEC handles it
- Lights go off last so you're not in the dark while the system shuts down

---

## Step 9 — Verification Checklist

After integration, test each of these:

- [ ] `media_player.tv_<room>` can power on (WoL) and off (`system/turnOff`)
- [ ] TV input switches to correct HDMI source
- [ ] TV sound output is `external_arc`
- [ ] `media_player.avr_<room>` can power on and shows correct source
- [ ] AVR volume responds to `media_player.volume_set`
- [ ] Apple TV shows current playback state
- [ ] Power-on script completes in ~20s with correct final state
- [ ] Power-off script cleanly shuts down all devices (~7s)
- [ ] CEC chain works: TV off cascades AVR to standby
- [ ] Light sync activates and deactivates correctly
- [ ] Audio is multichannel (not 2ch stereo) — check AVR display

---

## Master Cinema — Differences from Theatre

Things to investigate before starting:

1. **No VRROOM in the chain** (unless Master Cinema uses the VRROOM TX1 distribution output). The signal chain is likely simpler: Apple TV → HSB → TV → eARC → AVR.
2. **AVR source names**: MRX-540 may have different source names than MRX-740. Check `state_attr('media_player.avr_master', 'source_list')`.
3. **Master Cinema is in the Master Suite** — respect the master suite exclusion from global service activation.
4. **HSB identity**: Find which HSB is assigned to Master Cinema (check `ha_search_entities` for "master cinema" sync entities).
5. **12 sub-rooms in Master Suite** — make sure entities go to "Master Cinema" area specifically, not the parent "Master Suite".
6. **ATV-MasterBedroom** at 192.168.1.76 — may serve both bedroom and cinema. Clarify with user.

---

## Deferred / TODO (applies to all rooms)

- **Multichannel audio**: Theatre still at 2ch stereo. Likely needs VRROOM EDID `audiotx0` → `allaudio`. Master Cinema (no VRROOM) may work natively.
- **VRROOM diagnostic entities**: 11 disabled sensors to enable for audio diagnosis.
- **HSB entertainment areas**: Must be configured in Hue app (not HA) per room.
- **AVR-Sunroom**: MRX SLM not compatible with `anthemav` integration — awaiting update.
