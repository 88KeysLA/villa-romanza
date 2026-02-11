"""Shared fixtures for system health tests."""

import os
import pytest
import httpx


@pytest.fixture(scope="session")
def ha_token():
    token = os.environ.get("HA_TOKEN")
    if not token:
        pytest.skip("HA_TOKEN environment variable not set")
    return token


@pytest.fixture(scope="session")
def crestron_token():
    return os.environ.get("CRESTRON_TOKEN", "TLkVgJbnF8bk")


@pytest.fixture(scope="session")
def ha_base_url():
    return "http://192.168.1.6:8123"


@pytest.fixture(scope="session")
def crestron_base_url():
    return "https://192.168.1.2"


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
