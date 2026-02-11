"""Volume control tools with 70% safety cap per constitution."""

from ..server import mcp, speaker_cache, ha_client, resolver
from ..helpers import run_soco, clamp_volume
from ..integrations.home_assistant import check_agent_media_gate
from .playback import _resolve_device


@mcp.tool()
async def sonos_get_volume(speaker: str) -> dict:
    """Get current volume level and mute state of a speaker.

    Args:
        speaker: Speaker name
    """
    device = await _resolve_device(speaker)
    volume = await run_soco(lambda: device.volume)
    muted = await run_soco(lambda: device.mute)
    name = await run_soco(lambda: device.player_name)
    return {"speaker": name, "volume": volume, "muted": muted, "max_allowed": 70}


@mcp.tool()
async def sonos_set_volume(speaker: str, volume: int) -> str:
    """Set volume on a speaker (0-70). Values above 70 are clamped per safety rules.

    Args:
        speaker: Speaker name
        volume: Volume level 0-70
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    clamped, was_clamped = clamp_volume(volume)
    await run_soco(lambda: setattr(device, 'volume', clamped))
    name = await run_soco(lambda: device.player_name)
    msg = f"Volume set to {clamped}% on {name}"
    if was_clamped:
        msg += f" (requested {volume}%, clamped to {clamped}% per safety rules)"
    return msg


@mcp.tool()
async def sonos_set_relative_volume(speaker: str, adjustment: int) -> str:
    """Adjust volume up or down relative to current level. Result clamped to 0-70.

    Args:
        speaker: Speaker name
        adjustment: Volume change (-70 to +70, e.g. +5 or -10)
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    current = await run_soco(lambda: device.volume)
    target = current + adjustment
    clamped, was_clamped = clamp_volume(target)
    await run_soco(lambda: setattr(device, 'volume', clamped))
    name = await run_soco(lambda: device.player_name)
    msg = f"Volume {current}% → {clamped}% on {name}"
    if was_clamped:
        msg += f" (clamped from {target}%)"
    return msg


@mcp.tool()
async def sonos_mute(speaker: str, mute: bool) -> str:
    """Mute or unmute a speaker.

    Args:
        speaker: Speaker name
        mute: True to mute, False to unmute
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    await run_soco(lambda: setattr(device, 'mute', mute))
    name = await run_soco(lambda: device.player_name)
    return f"{'Muted' if mute else 'Unmuted'} {name}"
