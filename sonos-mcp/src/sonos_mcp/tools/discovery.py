"""Discovery tools: find and inspect Sonos speakers."""

from ..server import mcp, speaker_cache
from ..helpers import run_soco, format_speaker_state, format_markdown_speakers


@mcp.tool()
async def sonos_discover(force_refresh: bool = False) -> dict:
    """Discover all Sonos speakers on the network.

    Returns online speakers with IPs and offline speakers from the registry.
    Use force_refresh=True to bypass the 5-minute cache.
    """
    if force_refresh or speaker_cache.is_stale:
        await speaker_cache.discover()

    online = {}
    for name, device in speaker_cache.online.items():
        try:
            online[name] = {
                "ip": device.ip_address,
                "model": await run_soco(lambda d=device: d.model_name),
            }
        except Exception:
            online[name] = {"ip": getattr(device, "ip_address", "unknown"), "model": "unknown"}

    return {
        "online_count": len(online),
        "offline_count": len(speaker_cache.offline_names),
        "online": online,
        "offline": speaker_cache.offline_names,
    }


@mcp.tool()
async def sonos_get_speaker(speaker: str) -> dict:
    """Get full state of a specific speaker: volume, track, group, transport state.

    Args:
        speaker: Speaker name (e.g. "Lounge", "Kitchen", "Pool North")
    """
    from ..resolver import SpeakerResolver
    from ..server import resolver

    await speaker_cache.ensure_fresh()

    # Try direct match first
    device = speaker_cache.get(speaker)
    if not device:
        # Try fuzzy resolve
        result = resolver.resolve(speaker)
        if result.resolved and result.match_type == "speaker" and result.speaker_name:
            device = speaker_cache.get(result.speaker_name)

    if not device:
        return {"error": f"Speaker '{speaker}' not found. Online: {list(speaker_cache.online.keys())}"}

    state = await run_soco(format_speaker_state, device)
    return state


@mcp.tool()
async def sonos_system_status() -> str:
    """Get a markdown summary of all Sonos speakers: name, state, volume, track, group."""
    await speaker_cache.ensure_fresh()

    states = []
    for name, device in speaker_cache.online.items():
        state = await run_soco(format_speaker_state, device)
        states.append(state)

    md = format_markdown_speakers(states)
    if speaker_cache.offline_names:
        md += f"\n\n**Offline:** {', '.join(speaker_cache.offline_names)}"
    return md
