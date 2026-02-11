"""Villa Romanza Sonos MCP Server — entry point."""

import os
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP

from .discovery import SpeakerCache
from .resolver import SpeakerResolver
from .integrations.home_assistant import HomeAssistantClient
from .integrations.crestron import CrestronAwareness
from .config import SPEAKERS

# Module-level singletons (accessed by tool modules)
speaker_cache = SpeakerCache()
ha_client: HomeAssistantClient | None = None
crestron = CrestronAwareness()
resolver = SpeakerResolver()


@asynccontextmanager
async def app_lifespan(app):
    """Initialize SoCo discovery, HA client on startup; clean up on shutdown."""
    global ha_client, crestron

    ha_url = os.environ.get("HA_URL", "")
    ha_token = os.environ.get("HA_TOKEN", "")
    crestron_host = os.environ.get("CRESTRON_HOST", "192.168.1.2")
    crestron_token = os.environ.get("CRESTRON_AUTH_TOKEN", "")

    # HA client (optional — server works without it for standalone testing)
    if ha_url and ha_token:
        ha_client = HomeAssistantClient(ha_url, ha_token)
        await ha_client.initialize()

    # Crestron awareness (Phase 2 stub)
    crestron = CrestronAwareness(crestron_host, crestron_token)

    # Initial speaker discovery
    try:
        await speaker_cache.discover(SPEAKERS)
    except Exception:
        pass  # Discovery may fail if no speakers reachable; tools will retry

    yield

    # Cleanup
    if ha_client:
        await ha_client.close()


mcp = FastMCP("Villa Media Engine", lifespan=app_lifespan)

# Import tool modules to register all @mcp.tool() decorated functions
from .tools import register_all_tools  # noqa: E402
register_all_tools(mcp)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
