"""Speaker/zone resolution tool for natural language matching."""

from ..server import mcp, resolver


@mcp.tool()
async def sonos_resolve(utterance: str) -> dict:
    """Resolve a natural language description to a speaker or zone.

    Useful for understanding what speaker or zone a user means when they say
    things like "dining room", "pool area", "everywhere", "master suite".

    Args:
        utterance: Natural language input (e.g. "dining room", "pool", "everywhere")
    """
    result = resolver.resolve(utterance)
    return result.model_dump()
