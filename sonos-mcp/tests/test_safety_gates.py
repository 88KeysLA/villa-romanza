"""Test Home Assistant safety gate enforcement."""

import pytest
from unittest.mock import AsyncMock
from sonos_mcp.integrations.home_assistant import check_agent_media_gate

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_gate_passes_when_ha_is_none():
    """Standalone mode (no HA) should not block."""
    await check_agent_media_gate(None)


@pytest.mark.asyncio
async def test_gate_passes_when_enabled(mock_ha_client):
    """Agent media enabled → should pass."""
    mock_ha_client.is_agent_media_enabled = AsyncMock(return_value=True)
    await check_agent_media_gate(mock_ha_client)


@pytest.mark.asyncio
async def test_gate_blocks_when_disabled(mock_ha_client):
    """Agent media disabled → should raise ValueError."""
    mock_ha_client.is_agent_media_enabled = AsyncMock(return_value=False)
    with pytest.raises(ValueError, match="Agent media control is disabled"):
        await check_agent_media_gate(mock_ha_client)
