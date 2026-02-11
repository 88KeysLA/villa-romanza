"""Favorites and content tools: browse/play Sonos Favorites, search TuneIn."""

from typing import Optional
from ..server import mcp, speaker_cache, ha_client
from ..helpers import run_soco
from ..integrations.home_assistant import check_agent_media_gate
from ..music.favorites import SonosFavoritesService
from ..music.tunein import TuneInService
from .playback import _resolve_device


def _get_any_device():
    """Return any online SoCo device (needed for favorites/service queries)."""
    devices = speaker_cache.online
    if not devices:
        return None
    return next(iter(devices.values()))


@mcp.tool()
async def sonos_list_favorites() -> list:
    """List all Sonos Favorites. These may include content from Amazon Music,
    Spotify, TuneIn, or other services linked to the Sonos account."""
    await speaker_cache.ensure_fresh()
    service = SonosFavoritesService(_get_any_device)
    result = await service.browse()
    return [item.model_dump() for item in result.items]


@mcp.tool()
async def sonos_play_favorite(speaker: str, favorite: str) -> str:
    """Play a Sonos Favorite by name (fuzzy matching supported).

    This is the primary way to play Amazon Music content — save it as a
    Sonos Favorite first, then play it here.

    Args:
        speaker: Speaker name to play on
        favorite: Name of the Sonos Favorite (fuzzy match, e.g. "jazz playlist")
    """
    await check_agent_media_gate(ha_client)
    await speaker_cache.ensure_fresh()
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)

    service = SonosFavoritesService(_get_any_device)
    result = await service.search(favorite, limit=1)
    if not result.items:
        all_favs = await service.browse()
        names = [f.title for f in all_favs.items[:20]]
        return f"No favorite matching '{favorite}'. Available: {', '.join(names)}"

    best = result.items[0]
    uri = await service.get_playable_uri(best.item_id)
    if not uri:
        return f"Found '{best.title}' but could not resolve playable URI."

    # SoCo needs the metadata to display correctly
    await run_soco(coordinator.play_uri, uri, title=best.title)
    name = await run_soco(lambda: device.player_name)
    return f"Playing favorite '{best.title}' on {name}"


@mcp.tool()
async def sonos_search_tunein(query: str) -> list:
    """Search TuneIn radio stations by name or genre.

    Args:
        query: Search term (e.g. "jazz", "BBC", "classical")
    """
    await speaker_cache.ensure_fresh()
    service = TuneInService(_get_any_device)
    if not await service.is_available():
        return [{"error": "TuneIn service not available"}]
    result = await service.search(query, limit=10)
    return [item.model_dump() for item in result.items]


@mcp.tool()
async def sonos_play_tunein(speaker: str, station: str) -> str:
    """Play a TuneIn radio station on a speaker.

    Args:
        speaker: Speaker name
        station: Station name to search for and play
    """
    await check_agent_media_gate(ha_client)
    await speaker_cache.ensure_fresh()
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)

    service = TuneInService(_get_any_device)
    result = await service.search(station, limit=1)
    if not result.items:
        return f"No TuneIn station found for '{station}'"

    best = result.items[0]
    uri = await service.get_playable_uri(best.item_id)
    if not uri:
        return f"Found '{best.title}' but could not resolve playable URI."

    await run_soco(coordinator.play_uri, uri, title=best.title)
    name = await run_soco(lambda: device.player_name)
    return f"Playing TuneIn station '{best.title}' on {name}"
