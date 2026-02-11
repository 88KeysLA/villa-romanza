"""Tool registration for all Sonos MCP tools."""


def register_all_tools(mcp):
    """Import all tool modules to trigger @mcp.tool() registration."""
    from . import discovery
    from . import playback
    from . import volume
    from . import grouping
    from . import queue
    from . import favorites
    from . import zones
    from . import villa
    from . import resolve
