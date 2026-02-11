"""Playback control tools: play, pause, stop, next, previous, seek, play_uri."""

from ..server import mcp, speaker_cache, ha_client, resolver
from ..helpers import run_soco
from ..integrations.home_assistant import check_agent_media_gate


async def _resolve_device(speaker: str):
    """Resolve speaker name to SoCo device, using fuzzy matching if needed."""
    await speaker_cache.ensure_fresh()
    device = speaker_cache.get(speaker)
    if not device:
        result = resolver.resolve(speaker)
        if result.resolved and result.match_type == "speaker" and result.speaker_name:
            device = speaker_cache.get(result.speaker_name)
    if not device:
        raise ValueError(f"Speaker '{speaker}' not found. Available: {list(speaker_cache.online.keys())}")
    return device


@mcp.tool()
async def sonos_play(speaker: str) -> str:
    """Resume playback on a speaker.

    Args:
        speaker: Speaker name (e.g. "Lounge", "Kitchen")
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.play)
    return f"Playing on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_pause(speaker: str) -> str:
    """Pause playback on a speaker.

    Args:
        speaker: Speaker name
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.pause)
    return f"Paused {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_stop(speaker: str) -> str:
    """Stop playback on a speaker.

    Args:
        speaker: Speaker name
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.stop)
    return f"Stopped {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_next(speaker: str) -> str:
    """Skip to next track on a speaker.

    Args:
        speaker: Speaker name
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.next)
    return f"Skipped to next on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_previous(speaker: str) -> str:
    """Skip to previous track on a speaker.

    Args:
        speaker: Speaker name
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.previous)
    return f"Previous track on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_seek(speaker: str, position: str) -> str:
    """Seek to a position in the current track.

    Args:
        speaker: Speaker name
        position: Time position in HH:MM:SS format (e.g. "0:01:30" for 1min 30sec)
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.seek, position)
    return f"Seeked to {position} on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_play_uri(speaker: str, uri: str, title: str = "") -> str:
    """Play an HTTP stream URL or audio file on a speaker.

    Supports http://, https://, x-rincon-mp3radio:// and other Sonos URI formats.
    Use this for internet radio, generative music streams, or direct audio files.

    Args:
        speaker: Speaker name
        uri: Audio URI to play
        title: Optional display title
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.play_uri, uri, title=title)
    name = await run_soco(lambda: device.player_name)
    return f"Playing {title or uri} on {name}"
