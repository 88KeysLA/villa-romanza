"""Shared fixtures for sonos-mcp tests."""

import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock

# Ensure sonos_mcp is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def mock_soco():
    """Mock SoCo device."""
    device = MagicMock()
    device.player_name = "Test Speaker"
    device.ip_address = "192.168.0.100"
    device.volume = 30
    device.mute = False
    device.is_coordinator = True
    device.model_name = "Sonos One"
    device.get_current_transport_info.return_value = {
        "current_transport_state": "PLAYING",
    }
    device.get_current_track_info.return_value = {
        "title": "Test Track",
        "artist": "Test Artist",
        "album": "Test Album",
        "uri": "x-sonos-spotify:track",
        "duration": "0:03:45",
        "position": "0:01:23",
        "album_art_uri": "",
    }
    device.group = MagicMock()
    device.group.coordinator = device
    device.group.members = [device]
    return device


@pytest.fixture
def mock_ha_client():
    """Mock Home Assistant client."""
    client = AsyncMock()
    client.get_state = AsyncMock(return_value={"state": "on"})
    client.get_villa_mode = AsyncMock(return_value="NORMAL")
    client.is_agent_media_enabled = AsyncMock(return_value=True)
    client.get_autonomy_phase = AsyncMock(return_value="manual")
    return client
