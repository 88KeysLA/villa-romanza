"""Test helper functions: volume clamping, formatting."""

import pytest
from sonos_mcp.helpers import (
    clamp_volume, truncate_response, format_track_info,
    format_speaker_state, format_markdown_speakers,
)
from sonos_mcp.config import VOLUME_HARD_MAX

pytestmark = pytest.mark.unit


class TestClampVolume:

    def test_above_max(self):
        vol, clamped = clamp_volume(100)
        assert vol == VOLUME_HARD_MAX
        assert clamped is True

    def test_below_zero(self):
        vol, clamped = clamp_volume(-10)
        assert vol == 0
        assert clamped is True

    def test_in_range(self):
        vol, clamped = clamp_volume(50)
        assert vol == 50
        assert clamped is False

    def test_at_max_boundary(self):
        vol, clamped = clamp_volume(VOLUME_HARD_MAX)
        assert vol == VOLUME_HARD_MAX
        assert clamped is False

    def test_at_zero(self):
        vol, clamped = clamp_volume(0)
        assert vol == 0
        assert clamped is False

    def test_just_above_max(self):
        vol, clamped = clamp_volume(VOLUME_HARD_MAX + 1)
        assert vol == VOLUME_HARD_MAX
        assert clamped is True


class TestTruncateResponse:

    def test_short_text_unchanged(self):
        text = "Short text"
        assert truncate_response(text) == text

    def test_long_text_truncated(self):
        text = "x" * 30000
        result = truncate_response(text, limit=1000)
        assert len(result) <= 1000

    def test_exactly_at_limit(self):
        text = "x" * 25000
        result = truncate_response(text)
        assert result == text


class TestFormatTrackInfo:

    def test_basic_format(self):
        info = {
            "title": "Song", "artist": "Band", "album": "Album",
            "uri": "x-sonos:track", "duration": "0:03:00",
            "position": "0:01:00", "album_art_uri": "",
        }
        result = format_track_info(info)
        assert result["title"] == "Song"
        assert result["artist"] == "Band"
        assert result["album"] == "Album"

    def test_missing_fields(self):
        result = format_track_info({})
        assert result["title"] == ""
        assert result["artist"] == ""


class TestFormatSpeakerState:

    def test_normal_device(self, mock_soco):
        state = format_speaker_state(mock_soco)
        assert state["name"] == "Test Speaker"
        assert state["volume"] == 30
        assert state["state"] == "PLAYING"
        assert state["is_coordinator"] is True

    def test_error_handling(self):
        """Broken device returns error dict instead of crashing."""
        bad = type("Bad", (), {"player_name": "Bad", "ip_address": "0.0.0.0"})()
        bad.get_current_transport_info = lambda: (_ for _ in ()).throw(Exception("fail"))
        state = format_speaker_state(bad)
        assert "error" in state


class TestFormatMarkdownSpeakers:

    def test_produces_table(self):
        speakers = [{
            "name": "Library", "state": "PLAYING", "volume": 30,
            "muted": False, "track": {"title": "Song", "artist": "Band"},
            "is_coordinator": True, "group_members": ["Library"],
            "group_coordinator": "Library",
        }]
        result = format_markdown_speakers(speakers)
        assert "| Speaker |" in result
        assert "Library" in result
        assert "PLAYING" in result

    def test_error_speaker(self):
        speakers = [{"name": "Broken", "error": "timeout"}]
        result = format_markdown_speakers(speakers)
        assert "ERROR" in result
        assert "timeout" in result
