"""Test UniFi reservation data integrity."""

import pytest
from dhcp_force_renew import RESERVATIONS_CORE, RESERVATIONS_LIGHTING, ALL_RESERVATIONS

pytestmark = pytest.mark.unit


class TestCoreReservations:

    def test_no_duplicate_macs(self):
        macs = [r[1] for r in RESERVATIONS_CORE]
        dupes = [m for m in macs if macs.count(m) > 1]
        assert len(macs) == len(set(macs)), f"Duplicate MACs: {set(dupes)}"

    def test_no_duplicate_ips(self):
        ips = [r[2] for r in RESERVATIONS_CORE]
        dupes = [ip for ip in ips if ips.count(ip) > 1]
        assert len(ips) == len(set(ips)), f"Duplicate IPs: {set(dupes)}"

    def test_ips_in_correct_subnet(self):
        for name, mac, ip in RESERVATIONS_CORE:
            assert ip.startswith("192.168.0.") or ip.startswith("192.168.1."), \
                f"{name} has IP {ip} outside Core VLAN"


class TestLightingReservations:

    def test_count(self):
        assert len(RESERVATIONS_LIGHTING) == 29, \
            f"Expected 29 Hue bridges, got {len(RESERVATIONS_LIGHTING)}"

    def test_no_duplicate_macs(self):
        macs = [r[1] for r in RESERVATIONS_LIGHTING]
        dupes = [m for m in macs if macs.count(m) > 1]
        assert len(macs) == len(set(macs)), f"Duplicate MACs: {set(dupes)}"

    def test_no_duplicate_ips(self):
        ips = [r[2] for r in RESERVATIONS_LIGHTING]
        dupes = [ip for ip in ips if ips.count(ip) > 1]
        assert len(ips) == len(set(ips)), f"Duplicate IPs: {set(dupes)}"

    def test_ips_in_lighting_subnet(self):
        for name, mac, ip in RESERVATIONS_LIGHTING:
            assert ip.startswith("192.168.20."), \
                f"{name} has IP {ip} outside Lighting VLAN"


class TestCrossVLAN:

    def test_no_mac_conflicts(self):
        core_macs = {r[1] for r in RESERVATIONS_CORE}
        lighting_macs = {r[1] for r in RESERVATIONS_LIGHTING}
        overlap = core_macs & lighting_macs
        assert len(overlap) == 0, f"MAC conflicts across VLANs: {overlap}"


class TestMACFormat:

    @pytest.mark.parametrize("name,mac,ip", ALL_RESERVATIONS[:10] + ALL_RESERVATIONS[-10:])
    def test_mac_format(self, name, mac, ip):
        """MAC should be lowercase, colon-separated, 6 octets."""
        assert mac == mac.lower(), f"{name} MAC not lowercase"
        parts = mac.split(":")
        assert len(parts) == 6, f"{name} MAC doesn't have 6 octets"
        for part in parts:
            assert len(part) == 2, f"{name} MAC octet '{part}' wrong length"
            int(part, 16)  # Raises ValueError if not hex


class TestCriticalDevices:

    def test_vrroom_exists(self):
        vrroom = [r for r in RESERVATIONS_CORE if r[0] == "VRROOM"]
        assert len(vrroom) == 1
        assert vrroom[0][1] == "18:9b:a5:d4:12:cb"
        assert vrroom[0][2] == "192.168.1.70"

    def test_tvs_exist(self):
        tvs = [r for r in RESERVATIONS_CORE if r[0].startswith("TV-")]
        assert len(tvs) >= 5, f"Expected >=5 TVs, got {len(tvs)}"

    def test_sonos_speakers_exist(self):
        sonos = [r for r in RESERVATIONS_CORE if r[0].startswith("SNS-")]
        assert len(sonos) == 25, f"Expected 25 Sonos, got {len(sonos)}"

    def test_touch_panels_exist(self):
        tps = [r for r in RESERVATIONS_CORE if r[0].startswith("TP-")]
        assert len(tps) == 14, f"Expected 14 touch panels, got {len(tps)}"

    def test_avrs_exist(self):
        avrs = [r for r in RESERVATIONS_CORE if r[0].startswith("AVR-")]
        assert len(avrs) == 3, f"Expected 3 AVRs, got {len(avrs)}"

    def test_hue_bridges_exist(self):
        bridges = [r for r in RESERVATIONS_LIGHTING if r[0].startswith("HueB")]
        assert len(bridges) == 29, f"Expected 29 Hue bridges, got {len(bridges)}"
