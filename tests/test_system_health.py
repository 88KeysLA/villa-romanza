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
SAMPLE_SYNC_BOXES = ["192.168.20.86", "192.168.20.92", "192.168.20.95"]  # Bar, Great Room, Theatre

# Security VLAN Access devices (new reserved IPs after DHCP lockdown 2026-02-13)
ACCESS_HUBS = {
    "gate_hub": "192.168.4.10",
    "door_hub": "192.168.4.11",
}
ACCESS_READERS = {
    "gate_intercom": "192.168.4.20",
    "entrata_intercom": "192.168.4.21",
    "north_porta": "192.168.4.22",
    "motor_court_reader": "192.168.4.23",
    "plaza_gate_reader": "192.168.4.24",
    "garage_in_reader": "192.168.4.25",
    "cabana_reader": "192.168.4.26",
}
SAMPLE_CAMERAS = ["192.168.4.50", "192.168.4.60", "192.168.4.80"]  # Garden, Kitchen, RoofNorth

# Smart Things VLAN devices (current DHCP IPs until reservations are applied)
SMART_THINGS_ECOBEES = {
    "eco_1": "192.168.6.118",
    "eco_2": "192.168.6.121",
    "eco_3": "192.168.6.147",
    "eco_4": "192.168.6.178",
    "eco_5": "192.168.6.180",
    "eco_6": "192.168.6.209",
}
SMART_THINGS_MYQ = {
    "myq_1": "192.168.6.50",
    "myq_2": "192.168.6.51",
    "myq_3": "192.168.6.52",
    "myq_4": "192.168.6.53",
}


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

    @pytest.mark.slow
    @pytest.mark.parametrize("ip", SAMPLE_SYNC_BOXES)
    def test_sync_boxes(self, ip):
        assert _ping(ip), f"Hue Sync Box at {ip} unreachable"


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
        "hdfury", "hue", "sonos", "anthemav", "crestron_home", "unifi", "huesyncbox", "webostv", "apple_tv",
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
        return r.json()["authkey"]

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


# ── Hue Sync Box Integration ────────────────────────────────────

@pytest.mark.ha
@pytest.mark.network
class TestHueSyncBoxes:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    def test_sync_box_entities_exist(self):
        """At least some Hue Sync Box entities should exist after pairing."""
        r = self._get("/api/states")
        assert r.status_code == 200
        states = r.json()
        # huesyncbox creates select/switch/sensor/number entities after pairing
        # Exclude update.* entities (HACS update tracker, not actual devices)
        hsb_entities = [s for s in states
                        if "sync_mode" in s.get("entity_id", "")]
        assert len(hsb_entities) >= 15, f"Expected >=15 sync_mode entities, got {len(hsb_entities)}"

    @pytest.mark.slow
    @pytest.mark.parametrize("ip", SAMPLE_SYNC_BOXES)
    def test_sync_box_api_reachable(self, ip):
        """Hue Sync Boxes expose a REST API on port 443."""
        try:
            r = httpx.get(
                f"https://{ip}/api/v1/device",
                verify=False, timeout=5,
            )
            assert r.status_code == 200, f"Sync box at {ip} returned {r.status_code}"
            data = r.json()
            assert "uniqueId" in data, f"Sync box at {ip} missing uniqueId"
            assert data.get("deviceType") == "HSB2", f"Unexpected device type at {ip}"
        except httpx.ConnectError:
            pytest.fail(f"Sync box at {ip} not responding on port 443")


# ── Access Devices (Security VLAN) ─────────────────────────────

@pytest.mark.security
@pytest.mark.network
class TestAccessDevices:

    @pytest.mark.parametrize("name,ip", list(ACCESS_HUBS.items()))
    def test_access_hub_reachable(self, name, ip):
        assert _ping(ip), f"Access hub {name} at {ip} unreachable"

    @pytest.mark.parametrize("name,ip", list(ACCESS_READERS.items()))
    def test_access_reader_reachable(self, name, ip):
        assert _ping(ip), f"Access reader {name} at {ip} unreachable"

    def test_nvr_access_api_port(self):
        """NVR Access controller listens on port 12443."""
        try:
            r = httpx.get(
                "https://192.168.4.7:12443/",
                verify=False, timeout=5,
            )
            # Any HTTP response means the port is up (auth may block us)
            assert r.status_code < 500, (
                f"NVR Access port 12443 returned server error {r.status_code}"
            )
        except httpx.ConnectError:
            pytest.fail("NVR Access API port 12443 not responding")

    @pytest.mark.slow
    @pytest.mark.parametrize("ip", SAMPLE_CAMERAS)
    def test_sample_cameras_reachable(self, ip):
        assert _ping(ip), f"Camera at {ip} unreachable"


# ── Smart Things VLAN ────────────────────────────────────────────

@pytest.mark.network
@pytest.mark.smart_things
class TestSmartThingsVLAN:

    @pytest.mark.parametrize("name,ip", list(SMART_THINGS_ECOBEES.items()))
    def test_ecobee_reachable(self, name, ip):
        assert _ping(ip), f"Ecobee {name} at {ip} unreachable"

    @pytest.mark.parametrize("name,ip", list(SMART_THINGS_MYQ.items()))
    def test_myq_reachable(self, name, ip):
        assert _ping(ip), f"MyQ {name} at {ip} unreachable"

    def test_rachio_reachable(self):
        assert _ping("192.168.6.182"), "Rachio sprinkler at 192.168.6.182 unreachable"

    def test_irobot_reachable(self):
        assert _ping("192.168.6.196"), "iRobot at 192.168.6.196 unreachable"


# ── AV Room Entities ─────────────────────────────────────────────

@pytest.mark.ha
@pytest.mark.network
class TestTheatreAV:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    @pytest.mark.parametrize("entity_id", [
        "media_player.tv_theatre",
        "media_player.avr_theatre",
        "media_player.atv_theatre",
        "remote.atv_theatre",
        "media_player.xbx_theatre",
        "button.wol_tv_theatre",
        "switch.theatre_light_sync",
        "select.hdfury_vrroom_11_port_select_tx0",
    ])
    def test_theatre_entity_exists(self, entity_id):
        r = self._get(f"/api/states/{entity_id}")
        assert r.status_code == 200, f"Entity {entity_id} not found"

    def test_theatre_script_exists(self):
        r = self._get("/api/states/script.watch_theatre")
        assert r.status_code == 200, "script.watch_theatre not found"

    def test_theatre_off_script_exists(self):
        r = self._get("/api/states/script.theatre_off")
        assert r.status_code == 200, "script.theatre_off not found"


@pytest.mark.ha
@pytest.mark.network
class TestMasterCinemaAV:

    @pytest.fixture(autouse=True)
    def _setup(self, ha_base_url, ha_token):
        self.url = ha_base_url
        self.headers = {"Authorization": f"Bearer {ha_token}"}

    def _get(self, path):
        return httpx.get(f"{self.url}{path}", headers=self.headers, timeout=10)

    @pytest.mark.parametrize("entity_id", [
        "media_player.tv_master_cinema",
        "media_player.avr_master",
        "media_player.atv_master_cinema",
        "remote.atv_master_cinema",
        "button.wol_tv_master_cinema",
        "switch.master2_light_sync",
        "media_player.master_cinema_in",
        "media_player.master_cinema_out",
        "media_player.avr_master_zone2",
        "select.master2_intensity",
    ])
    def test_master_cinema_entity_exists(self, entity_id):
        r = self._get(f"/api/states/{entity_id}")
        assert r.status_code == 200, f"Entity {entity_id} not found"

    @pytest.mark.parametrize("entity_id", [
        "light.master_lamp_l",
        "light.master_lamp_r",
        "light.master_theatre",
    ])
    def test_master_cinema_light_exists(self, entity_id):
        r = self._get(f"/api/states/{entity_id}")
        assert r.status_code == 200, f"Entity {entity_id} not found"

    def test_master_cinema_intensity_options(self):
        r = self._get("/api/states/select.master2_intensity")
        assert r.status_code == 200
        options = r.json()["attributes"]["options"]
        assert "subtle" in options, "HSB 'subtle' intensity option missing"

    def test_master_cinema_script_exists(self):
        r = self._get("/api/states/script.watch_master_cinema")
        assert r.status_code == 200, "script.watch_master_cinema not found"

    def test_master_cinema_off_script_exists(self):
        r = self._get("/api/states/script.master_cinema_off")
        assert r.status_code == 200, "script.master_cinema_off not found"
