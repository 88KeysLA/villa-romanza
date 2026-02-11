"""Test speaker registry and zone definitions."""

import pytest
from sonos_mcp.config import SPEAKERS, ZONES, VOLUME_HARD_MAX, HA_ONLY_SPEAKERS

pytestmark = pytest.mark.unit


class TestSpeakerRegistry:

    def test_speaker_count(self):
        assert len(SPEAKERS) == 25

    def test_no_duplicate_ips(self):
        ips = [s.ip for s in SPEAKERS.values()]
        assert len(ips) == len(set(ips)), f"Duplicate IPs: {[ip for ip in ips if ips.count(ip) > 1]}"

    def test_no_duplicate_names(self):
        names = list(SPEAKERS.keys())
        assert len(names) == len(set(names))

    def test_all_ips_in_core_vlan(self):
        for name, info in SPEAKERS.items():
            assert info.ip.startswith("192.168.0."), f"{name} IP {info.ip} not in Core VLAN"

    def test_all_ips_in_sonos_range(self):
        for name, info in SPEAKERS.items():
            last = int(info.ip.split(".")[-1])
            assert 100 <= last <= 125, f"{name} IP {info.ip} outside .100-.125"

    def test_ha_entity_format(self):
        for name, info in SPEAKERS.items():
            assert info.ha_entity.startswith("media_player."), f"{name}: {info.ha_entity}"
            assert " " not in info.ha_entity

    def test_network_names_start_with_sns(self):
        for name, info in SPEAKERS.items():
            assert info.network_name.startswith("SNS-"), f"{name}: {info.network_name}"

    def test_all_have_rooms(self):
        for name, info in SPEAKERS.items():
            assert info.room, f"{name} missing room"


class TestZoneDefinitions:

    def test_zone_count(self):
        assert len(ZONES) == 8

    def test_all_zones_have_coordinators(self):
        for zid, zone in ZONES.items():
            assert zone.default_coordinator, f"Zone {zid} missing coordinator"

    def test_coordinator_exists(self):
        all_names = set(SPEAKERS.keys()) | set(HA_ONLY_SPEAKERS.keys())
        for zid, zone in ZONES.items():
            assert zone.default_coordinator in all_names, \
                f"Zone {zid} coordinator '{zone.default_coordinator}' not in registry"

    def test_zone_speakers_exist(self):
        all_names = set(SPEAKERS.keys()) | set(HA_ONLY_SPEAKERS.keys())
        for zid, zone in ZONES.items():
            if zone.speakers == ["ALL"]:
                continue
            for speaker in zone.speakers:
                assert speaker in all_names, \
                    f"Zone {zid} references unknown speaker '{speaker}'"

    def test_whole_house_is_all(self):
        assert "whole_house" in ZONES
        assert ZONES["whole_house"].speakers == ["ALL"]

    def test_zone_max_volume_within_hard_max(self):
        for zid, zone in ZONES.items():
            assert zone.max_volume <= VOLUME_HARD_MAX, \
                f"Zone {zid} max_volume {zone.max_volume} > {VOLUME_HARD_MAX}"


class TestSafetyConstants:

    def test_volume_hard_max_is_70(self):
        """Constitution Section B.2: max 70%."""
        assert VOLUME_HARD_MAX == 70
