"""Villa integration tools: mode context, now-playing summary."""

from typing import Optional
from ..server import mcp, speaker_cache, ha_client
from ..helpers import run_soco, format_track_info


@mcp.tool()
async def sonos_villa_context() -> dict:
    """Get current villa context: mode, agent media gate, and per-speaker summary.

    Returns villa_mode, agent_media_enabled, and a compact now-playing for each speaker.
    """
    context = {
        "villa_mode": "UNKNOWN",
        "agent_media_enabled": False,
        "speakers": {},
    }

    if ha_client:
        try:
            context["villa_mode"] = await ha_client.get_villa_mode()
        except Exception:
            pass
        try:
            context["agent_media_enabled"] = await ha_client.is_agent_media_enabled()
        except Exception:
            pass

    await speaker_cache.ensure_fresh()
    for name, device in speaker_cache.online.items():
        try:
            transport = await run_soco(lambda d=device: d.get_current_transport_info())
            track = await run_soco(lambda d=device: d.get_current_track_info())
            vol = await run_soco(lambda d=device: d.volume)
            context["speakers"][name] = {
                "state": transport.get("current_transport_state", "UNKNOWN"),
                "volume": vol,
                "track": track.get("title", ""),
                "artist": track.get("artist", ""),
            }
        except Exception:
            context["speakers"][name] = {"state": "ERROR"}

    return context


@mcp.tool()
async def sonos_now_playing(speaker: Optional[str] = None) -> dict:
    """Get current track info for one speaker or all speakers.

    Args:
        speaker: Optional speaker name. If omitted, returns all speakers.
    """
    await speaker_cache.ensure_fresh()

    if speaker:
        from .playback import _resolve_device
        device = await _resolve_device(speaker)
        track = await run_soco(lambda: device.get_current_track_info())
        transport = await run_soco(lambda: device.get_current_transport_info())
        return {
            "speaker": await run_soco(lambda: device.player_name),
            "state": transport.get("current_transport_state", "UNKNOWN"),
            **format_track_info(track),
        }

    # All speakers
    result = {}
    for name, device in speaker_cache.online.items():
        try:
            track = await run_soco(lambda d=device: d.get_current_track_info())
            transport = await run_soco(lambda d=device: d.get_current_transport_info())
            result[name] = {
                "state": transport.get("current_transport_state", "UNKNOWN"),
                **format_track_info(track),
            }
        except Exception:
            result[name] = {"state": "ERROR"}
    return result
