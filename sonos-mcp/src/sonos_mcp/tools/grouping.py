"""Speaker grouping tools: join, unjoin, create groups, party mode."""

from typing import List
from ..server import mcp, speaker_cache, ha_client, resolver
from ..helpers import run_soco
from ..integrations.home_assistant import check_agent_media_gate
from .playback import _resolve_device


@mcp.tool()
async def sonos_list_groups() -> list:
    """List all current Sonos speaker groups with coordinators and members."""
    await speaker_cache.ensure_fresh()

    seen_groups = set()
    groups = []
    for name, device in speaker_cache.online.items():
        try:
            group = await run_soco(lambda d=device: d.group)
            coord_name = await run_soco(lambda g=group: g.coordinator.player_name)
            if coord_name in seen_groups:
                continue
            seen_groups.add(coord_name)
            members = await run_soco(lambda g=group: [m.player_name for m in g.members])
            groups.append({
                "coordinator": coord_name,
                "members": members,
                "size": len(members),
            })
        except Exception:
            continue

    return groups


@mcp.tool()
async def sonos_join(speaker: str, coordinator: str) -> str:
    """Join a speaker to another speaker's group. The coordinator controls playback.

    Args:
        speaker: Speaker to join (will follow the coordinator)
        coordinator: Speaker that controls playback for the group
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    coord_device = await _resolve_device(coordinator)
    await run_soco(device.join, coord_device)
    s_name = await run_soco(lambda: device.player_name)
    c_name = await run_soco(lambda: coord_device.player_name)
    return f"{s_name} joined group led by {c_name}"


@mcp.tool()
async def sonos_unjoin(speaker: str) -> str:
    """Remove a speaker from its current group (becomes independent).

    Args:
        speaker: Speaker to remove from group
    """
    await check_agent_media_gate(ha_client)
    device = await _resolve_device(speaker)
    await run_soco(device.unjoin)
    name = await run_soco(lambda: device.player_name)
    return f"{name} removed from group (now solo)"


@mcp.tool()
async def sonos_create_group(coordinator: str, members: List[str]) -> str:
    """Create a new speaker group from a coordinator and list of members.

    Args:
        coordinator: Speaker that will control playback
        members: List of speaker names to add to the group
    """
    await check_agent_media_gate(ha_client)
    coord_device = await _resolve_device(coordinator)
    joined = []
    errors = []
    for member_name in members:
        try:
            member_device = await _resolve_device(member_name)
            await run_soco(member_device.join, coord_device)
            joined.append(member_name)
        except Exception as e:
            errors.append(f"{member_name}: {e}")

    c_name = await run_soco(lambda: coord_device.player_name)
    msg = f"Group created: {c_name} (coordinator) + {', '.join(joined)}"
    if errors:
        msg += f"\nFailed: {'; '.join(errors)}"
    return msg


@mcp.tool()
async def sonos_party_mode(coordinator: str = "Lounge") -> str:
    """Put ALL speakers into one group (party mode). Use with care.

    Args:
        coordinator: Speaker to be the group coordinator (default: Lounge)
    """
    await check_agent_media_gate(ha_client)
    coord_device = await _resolve_device(coordinator)
    await run_soco(coord_device.partymode)
    c_name = await run_soco(lambda: coord_device.player_name)
    return f"Party mode activated! All speakers grouped under {c_name}"
