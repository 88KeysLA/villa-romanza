"""Zone management tools: predefined speaker zones for the villa."""

from typing import Optional
from ..server import mcp, speaker_cache, ha_client, resolver
from ..config import ZONES
from ..helpers import run_soco, format_speaker_state, clamp_volume
from ..integrations.home_assistant import check_agent_media_gate
from .playback import _resolve_device


@mcp.tool()
async def sonos_list_zones() -> list:
    """List all predefined speaker zones with their members."""
    zones = []
    for zid, zone in ZONES.items():
        zones.append({
            "zone_id": zid,
            "display_name": zone.display_name,
            "speakers": zone.speakers,
            "default_coordinator": zone.default_coordinator,
            "description": zone.description,
            "max_volume": zone.max_volume,
        })
    return zones


@mcp.tool()
async def sonos_play_in_zone(
    zone: str,
    favorite: Optional[str] = None,
    uri: Optional[str] = None,
    volume: Optional[int] = None,
) -> str:
    """Group all speakers in a zone and optionally play content at a set volume.

    This is the high-level "play music in a room" tool. It:
    1. Groups all zone speakers under the default coordinator
    2. Sets volume on all speakers (clamped to 70%)
    3. Plays the specified favorite or URI

    Args:
        zone: Zone ID (e.g. "great_room", "pool", "outdoor", "whole_house")
        favorite: Optional Sonos Favorite name to play
        uri: Optional HTTP stream URI to play (alternative to favorite)
        volume: Optional volume for all zone speakers (0-70)
    """
    await check_agent_media_gate(ha_client)
    await speaker_cache.ensure_fresh()

    zone_def = ZONES.get(zone)
    if not zone_def:
        # Try fuzzy resolve
        result = resolver.resolve(zone)
        if result.resolved and result.match_type == "zone" and result.zone_id:
            zone_def = ZONES.get(result.zone_id)
    if not zone_def:
        return f"Zone '{zone}' not found. Available: {list(ZONES.keys())}"

    # Handle whole_house special case
    if zone_def.speakers == ["ALL"]:
        coord_device = await _resolve_device(zone_def.default_coordinator)
        await run_soco(coord_device.partymode)
        speakers_grouped = list(speaker_cache.online.keys())
    else:
        coord_device = await _resolve_device(zone_def.default_coordinator)
        speakers_grouped = [zone_def.default_coordinator]
        for spk_name in zone_def.speakers:
            if spk_name == zone_def.default_coordinator:
                continue
            try:
                spk_device = await _resolve_device(spk_name)
                await run_soco(spk_device.join, coord_device)
                speakers_grouped.append(spk_name)
            except Exception:
                pass  # Speaker offline, skip

    # Set volume on all zone speakers
    if volume is not None:
        clamped, _ = clamp_volume(volume)
        for spk_name in speakers_grouped:
            try:
                spk_device = speaker_cache.get(spk_name) or await _resolve_device(spk_name)
                await run_soco(lambda d=spk_device, v=clamped: setattr(d, 'volume', v))
            except Exception:
                pass

    # Play content
    coordinator = await run_soco(lambda: coord_device.group.coordinator)
    content_msg = ""
    if favorite:
        from ..music.favorites import SonosFavoritesService
        from .favorites import _get_any_device
        svc = SonosFavoritesService(_get_any_device)
        result = await svc.search(favorite, limit=1)
        if result.items:
            fav_uri = await svc.get_playable_uri(result.items[0].item_id)
            if fav_uri:
                await run_soco(coordinator.play_uri, fav_uri, title=result.items[0].title)
                content_msg = f", playing '{result.items[0].title}'"
    elif uri:
        await run_soco(coordinator.play_uri, uri)
        content_msg = f", playing URI"

    vol_msg = f" at {volume}%" if volume else ""
    return (
        f"Zone '{zone_def.display_name}' active: {len(speakers_grouped)} speakers grouped"
        f"{vol_msg}{content_msg}"
    )


@mcp.tool()
async def sonos_zone_status(zone: str) -> dict:
    """Get the current status of a predefined zone: what's playing, volumes, group state.

    Args:
        zone: Zone ID (e.g. "great_room", "pool")
    """
    await speaker_cache.ensure_fresh()

    zone_def = ZONES.get(zone)
    if not zone_def:
        result = resolver.resolve(zone)
        if result.resolved and result.match_type == "zone" and result.zone_id:
            zone_def = ZONES.get(result.zone_id)
    if not zone_def:
        return {"error": f"Zone '{zone}' not found. Available: {list(ZONES.keys())}"}

    speaker_names = zone_def.speakers
    if speaker_names == ["ALL"]:
        speaker_names = list(speaker_cache.online.keys())

    states = []
    for name in speaker_names:
        device = speaker_cache.get(name)
        if device:
            state = await run_soco(format_speaker_state, device)
            states.append(state)
        else:
            states.append({"name": name, "error": "offline"})

    return {
        "zone": zone_def.display_name,
        "zone_id": zone_def.zone_id,
        "speakers": states,
    }
