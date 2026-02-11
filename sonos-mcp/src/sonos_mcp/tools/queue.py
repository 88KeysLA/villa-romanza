"""Queue management tools."""

from typing import Optional
from ..server import mcp, speaker_cache, ha_client
from ..helpers import run_soco
from ..integrations.home_assistant import check_agent_media_gate
from .playback import _resolve_device


@mcp.tool()
async def sonos_get_queue(speaker: str, offset: int = 0, limit: int = 20) -> dict:
    """Get the current play queue of a speaker.

    Args:
        speaker: Speaker name
        offset: Start position in queue (0-indexed)
        limit: Maximum items to return
    """
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    queue = await run_soco(coordinator.get_queue, offset, limit)

    items = []
    for item in queue:
        items.append({
            "title": item.title,
            "creator": getattr(item, "creator", ""),
            "album": getattr(item, "album", ""),
            "uri": item.resources[0].uri if item.resources else "",
        })

    total = await run_soco(lambda: coordinator.queue_size)
    return {
        "speaker": await run_soco(lambda: device.player_name),
        "total_in_queue": total,
        "offset": offset,
        "items": items,
    }


@mcp.tool()
async def sonos_clear_queue(speaker: str) -> str:
    """Clear the play queue of a speaker. This removes all queued tracks.

    Args:
        speaker: Speaker name
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.clear_queue)
    return f"Queue cleared on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_play_from_queue(speaker: str, index: int) -> str:
    """Play a specific item from the queue by index (0-based).

    Args:
        speaker: Speaker name
        index: Queue position to play (0 = first item)
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)
    await run_soco(coordinator.play_from_queue, index)
    return f"Playing queue item {index} on {await run_soco(lambda: device.player_name)}"


@mcp.tool()
async def sonos_set_play_mode(
    speaker: str,
    shuffle: Optional[bool] = None,
    repeat: Optional[str] = None,
) -> str:
    """Set shuffle and/or repeat mode on a speaker.

    Args:
        speaker: Speaker name
        shuffle: True/False to enable/disable shuffle
        repeat: "off", "one", or "all"
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coordinator = await run_soco(lambda: device.group.coordinator)

    # Build SoCo play_mode string
    current_mode = await run_soco(lambda: coordinator.play_mode)

    if shuffle is not None and repeat is not None:
        mode_map = {
            (False, "off"): "NORMAL",
            (True, "off"): "SHUFFLE_NOREPEAT",
            (False, "all"): "REPEAT_ALL",
            (True, "all"): "SHUFFLE",
            (False, "one"): "REPEAT_ONE",
            (True, "one"): "SHUFFLE_REPEAT_ONE",
        }
        new_mode = mode_map.get((shuffle, repeat), current_mode)
    elif shuffle is not None:
        new_mode = "SHUFFLE" if shuffle else "NORMAL"
    elif repeat is not None:
        repeat_map = {"off": "NORMAL", "all": "REPEAT_ALL", "one": "REPEAT_ONE"}
        new_mode = repeat_map.get(repeat, current_mode)
    else:
        return f"Current mode: {current_mode}"

    await run_soco(lambda: setattr(coordinator, 'play_mode', new_mode))
    return f"Play mode set to {new_mode} on {await run_soco(lambda: device.player_name)}"
