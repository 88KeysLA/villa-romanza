# Villa Romanza

Main Home Assistant configuration, MCP servers, tools, and tests for Villa Romanza.
Runs on **HA Green** (192.168.1.6).

## Architecture

```
villa-romanza/
  crestron-mcp/       # Crestron MCP server (CP4-R integration)
  sonos-mcp/          # Sonos MCP server (src/ + tests/)
  unifi-tools/        # UniFi network tools (DHCP force-renew, etc.)
  villa-motion-guard/ # Hue motion sensor toggle daemon (Mech Mac)
  docs/               # Network plans, security VLAN docs, system constitution
  tests/              # System health tests (HA connectivity, network)
```

## Key Files

- `crestron-mcp/crestron_mcp.py` — Crestron MCP server (CP4-R at 192.168.1.2, REST token `TLkVgJbnF8bk`).
- `sonos-mcp/src/` — Sonos MCP server source.
- `villa-motion-guard/motion_guard.py` — Watches `master_suite_mood` input_select, toggles 11 Hue motion sensors.
- `tests/test_system_health.py` — System health checks (network, HA API, device reachability).
- `unifi-tools/dhcp_force_renew.py` — Force DHCP renewal on UniFi devices.

## Test Commands

```bash
# Unit tests only (no network required)
PYTHONPATH=sonos-mcp/src pytest -v -m unit

# System health tests (requires HA_TOKEN)
export HA_TOKEN='your-token'
PYTHONPATH=sonos-mcp/src pytest tests/test_system_health.py -v

# All tests via runner script
./run_all_tests.sh --all
```

## Deploy

- **Crestron MCP**: Configured in Claude Desktop / Claude Code MCP settings, runs locally.
- **Motion Guard**: Deploy to Mech Mac (0.60) via `villa-motion-guard/deploy.sh`. LaunchDaemon `com.villaromanza.motion-guard`.
- **HA config changes**: Edit via HA MCP tools or HA REST API (not files in this repo directly).

## Notes

- HA YAML `off` must be quoted as `"off"` (parsed as boolean false otherwise).
- `media_player.turn_off` on LG TVs = Gallery mode, NOT standby. Use `webostv.command` `system/turnOff`.
- Hard Rule 4: Laundry and garage NEVER activated by global/domain service.
- Master suite excluded from global service activation.
