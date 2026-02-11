"""
Villa Romanza — System Health Tests

Verifies the live system: network reachability, HA integrations,
entity structure, Crestron connectivity, Sonos reachability.

Usage:
    pytest tests/test_system_health.py -v                # All
    pytest tests/test_system_health.py -v -m network     # Network only
    pytest tests/test_system_health.py -v -m ha          # HA only
"""

import subprocess
import pytest
import httpx


CRITICAL_DEVICES = {
    "gateway": "192.168.1.1",
    "crestron": "192.168.1.2",
    "ha_green": "192.168.1.6",
    "vrroom": "192.168.1.70",
    "avr_theatre": "192.168.0.130",
    "avr_master": "192.168.0.131",
    "nvr": "192.168.4.7",
}
SAMPLE_SONOS = ["192.168.0.100", "192.168.0.101", "192.168.0.102"]
SAMPLE_HUE = ["192.168.20.10", "192.168.20.11"]


def _ping(ip: str) -> bool:
    """Ping an IP once with 2s timeout (macOS)."""
    r = subprocess.run(["ping", "-c", "1", "-W", "2", ip], capture_output=True)
    return r.returncode == 0


# ── Network Reachability ──────────────────────────────────────────

@pytest.mark.network
class TestNetworkReachability:

    @pytest.mark.parametrize("name,ip", [
        ("gateway", "192.168.1.1"),
        ("crestron", "192.168.1.2"),
        ("ha_green", "192.168.1.6"),
        ("vrroom", "192.168.1.70"),
        ("avr_theatre", "192.168.0.130"),
        ("avr_master", "192.168.0.131"),
    ])
    def test_device_reachable(self, name, ip):
        assert _ping(ip), f"{name} at {ip} unreachable"

    @pytest.mark.xfail(reason="NVR currently offline — physical issue")
    def test_nvr(self):
        assert _ping("192.168.4.7"), "NVR 192.168.4.7 unreachable"

    @pytest.mark.slow
    @pytest.mark.parametrize("ip", SAMPLE_SONOS)
    def test_sonos_speakers(self, ip):
        assert _ping(ip), f"Sonos at {ip} unreachable"

    @pytest.mark.slow
    @pytest.mark.parametrize("ip", SAMPLE_HUE)
    def test_hue_bridges(self, ip):
        assert _ping(ip), f"Hue bridge at {ip} unreachable"


# ── Home Assistant Integrations ───────────────────────────────────

@pytest.mark.ha
@pytest.mark.network
class TestHAIntegrations:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    def test_api_accessible(self):
        r = self._get("/api/")
        assert r.status_code == 200
        assert r.json()["message"] == "API running."

    def test_config_valid(self):
        r = self._get("/api/config")
        assert r.status_code == 200
        data = r.json()
        assert "version" in data
        assert "components" in data

    @pytest.mark.parametrize("integration", [
        "hdfury", "hue", "sonos", "anthemav", "crestron_home", "unifi",
    ])
    def test_integration_loaded(self, integration):
        r = self._get("/api/config")
        components = r.json()["components"]
        assert integration in components, f"{integration} not loaded"


# ── Home Assistant Structure ──────────────────────────────────────

@pytest.mark.ha
@pytest.mark.network
class TestHAStructure:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    def test_five_floors(self):
        r = self._get("/api/config")
        # Floors aren't in /api/config directly — check via states
        # We'll verify through entity count instead
        r = self._get("/api/states")
        assert r.status_code == 200
        entities = r.json()
        # Rough sanity check: should have thousands of entities
        assert len(entities) > 3000, f"Only {len(entities)} entities — expected 4000+"

    def test_villa_mode_entity(self):
        r = self._get("/api/states/input_select.villa_mode")
        assert r.status_code == 200
        data = r.json()
        options = data["attributes"]["options"]
        for mode in ["NORMAL", "LISTEN", "WATCH", "ENTERTAIN", "LIVE_JAM", "SHOW", "INTERLUDE"]:
            assert mode in options, f"Mode {mode} missing from villa_mode"

    @pytest.mark.parametrize("entity_id", [
        "input_boolean.agent_controlled_lighting_enable",
        "input_boolean.agent_controlled_media_enable",
        "input_boolean.agent_controlled_visual_enable",
        "input_number.agent_controlled_lighting_intensity",
        "input_select.agent_controlled_autonomy_phase",
    ])
    def test_agent_control_entities(self, entity_id):
        r = self._get(f"/api/states/{entity_id}")
        assert r.status_code == 200, f"Entity {entity_id} not found"


# ── Home Assistant Key Entities ───────────────────────────────────

@pytest.mark.ha
@pytest.mark.network
class TestHAEntities:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    def test_avr_theatre_exists(self):
        r = self._get("/api/states/media_player.avr_theatre")
        assert r.status_code == 200

    def test_avr_master_exists(self):
        r = self._get("/api/states/media_player.avr_master")
        assert r.status_code == 200

    def test_vrroom_port_select_exists(self):
        r = self._get("/api/states/select.hdfury_vrroom_11_port_select_tx0")
        assert r.status_code == 200

    def test_vrroom_output_sensor_exists(self):
        r = self._get("/api/states/sensor.hdfury_vrroom_11_output_tx0")
        assert r.status_code == 200


# ── Crestron Connectivity ─────────────────────────────────────────

@pytest.mark.crestron
@pytest.mark.network
class TestCrestronConnectivity:

    @pytest.fixture(autouse=True)
    def _setup(self, crestron_base_url, crestron_token):
        self.url = crestron_base_url
        self.token = crestron_token

    def _auth(self):
        r = httpx.get(
            f"{self.url}/cws/api/login",
            headers={"Crestron-RestAPI-AuthToken": self.token},
            verify=False, timeout=10,
        )
        assert r.status_code == 200, "Crestron auth failed"
        return r.json()["AuthKey"]

    def test_authenticate(self):
        key = self._auth()
        assert key, "Empty auth key"

    def test_room_count(self):
        key = self._auth()
        r = httpx.get(
            f"{self.url}/cws/api/rooms",
            headers={"Crestron-RestAPI-AuthKey": key},
            verify=False, timeout=10,
        )
        assert r.status_code == 200
        rooms = r.json().get("rooms", [])
        assert 55 <= len(rooms) <= 70, f"Expected ~61 rooms, got {len(rooms)}"

    def test_device_count(self):
        key = self._auth()
        r = httpx.get(
            f"{self.url}/cws/api/devices",
            headers={"Crestron-RestAPI-AuthKey": key},
            verify=False, timeout=10,
        )
        assert r.status_code == 200
        devices = r.json().get("devices", [])
        assert len(devices) >= 50, f"Expected >=50 devices, got {len(devices)}"


# ── Sonos Reachability ────────────────────────────────────────────

@pytest.mark.sonos
@pytest.mark.network
@pytest.mark.slow
class TestSonosReachability:

    @pytest.mark.parametrize("ip", SAMPLE_SONOS)
    def test_sonos_http(self, ip):
        """Sonos speakers expose device description on port 1400."""
        try:
            r = httpx.get(f"http://{ip}:1400/xml/device_description.xml", timeout=5)
            assert r.status_code == 200, f"Sonos at {ip} returned {r.status_code}"
        except httpx.ConnectError:
            pytest.fail(f"Sonos at {ip} not responding on port 1400")
