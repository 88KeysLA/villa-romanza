"""Shared helpers: async SoCo wrapper, volume guard, agent gate, formatting."""

import asyncio
import json
from typing import Any, Callable, Optional
from .config import VOLUME_HARD_MAX, CHARACTER_LIMIT


async def run_soco(func: Callable, *args, **kwargs) -> Any:
    """Run a synchronous SoCo function in the thread pool executor."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


def clamp_volume(volume: int) -> tuple[int, bool]:
    """Clamp volume to 0-VOLUME_HARD_MAX. Returns (clamped, was_clamped)."""
    if volume > VOLUME_HARD_MAX:
        return VOLUME_HARD_MAX, True
    if volume < 0:
        return 0, True
    return volume, False


def truncate_response(text: str, limit: int = CHARACTER_LIMIT) -> str:
    """Truncate response text if it exceeds the character limit."""
    if len(text) <= limit:
        return text
    return text[:limit - 100] + f"\n\n... (truncated, {len(text) - limit + 100} chars omitted)"


def format_track_info(info: dict) -> dict:
    """Format SoCo track info dict into a clean response."""
    return {
        "title": info.get("title", ""),
        "artist": info.get("artist", ""),
        "album": info.get("album", ""),
        "uri": info.get("uri", ""),
        "duration": info.get("duration", "0:00:00"),
        "position": info.get("position", "0:00:00"),
        "album_art": info.get("album_art_uri", ""),
    }


def format_speaker_state(device) -> dict:
    """Build a state dict from a SoCo device instance."""
    try:
        transport = device.get_current_transport_info()
        track = device.get_current_track_info()
        group = device.group
        return {
            "name": device.player_name,
            "ip": device.ip_address,
            "volume": device.volume,
            "muted": device.mute,
            "state": transport.get("current_transport_state", "UNKNOWN"),
            "track": format_track_info(track),
            "is_coordinator": device.is_coordinator,
            "group_coordinator": group.coordinator.player_name if group else None,
            "group_members": [m.player_name for m in group.members] if group else [],
            "model": getattr(device, "model_name", ""),
        }
    except Exception as e:
        return {
            "name": getattr(device, "player_name", "unknown"),
            "ip": getattr(device, "ip_address", "unknown"),
            "error": str(e),
        }


def format_markdown_speakers(speakers: list[dict]) -> str:
    """Format a list of speaker states as a markdown table."""
    lines = ["| Speaker | State | Volume | Track | Group |",
             "|---|---|---|---|---|"]
    for s in speakers:
        if "error" in s:
            lines.append(f"| {s['name']} | ERROR | - | {s['error']} | - |")
        else:
            track_str = s["track"]["title"] or "-"
            if s["track"]["artist"]:
                track_str = f"{s['track']['artist']} — {track_str}"
            group_str = "solo"
            if len(s.get("group_members", [])) > 1:
                if s["is_coordinator"]:
                    group_str = f"coordinator ({len(s['group_members'])})"
                else:
                    group_str = f"→ {s['group_coordinator']}"
            mute_indicator = " (muted)" if s.get("muted") else ""
            lines.append(
                f"| {s['name']} | {s['state']} | {s['volume']}%{mute_indicator} "
                f"| {track_str} | {group_str} |"
            )
    return "\n".join(lines)
