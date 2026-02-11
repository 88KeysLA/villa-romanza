"""SoCo speaker discovery and cache management."""

import asyncio
import time
import soco
from typing import Dict, Optional, List
from .config import SPEAKERS, SpeakerInfo, DISCOVERY_CACHE_TTL


class SpeakerCache:
    """Manages SoCo device instances mapped to the speaker registry."""

    def __init__(self):
        self._devices: Dict[str, soco.SoCo] = {}
        self._by_ip: Dict[str, soco.SoCo] = {}
        self._last_discovery: float = 0
        self._offline: List[str] = []

    @property
    def is_stale(self) -> bool:
        return (time.time() - self._last_discovery) > DISCOVERY_CACHE_TTL

    async def discover(self, registry: Optional[Dict[str, SpeakerInfo]] = None) -> None:
        """Populate cache using network discovery + direct IP fallback."""
        reg = registry or SPEAKERS
        loop = asyncio.get_event_loop()

        # SoCo discover (SSDP/UPnP)
        discovered = await loop.run_in_executor(None, lambda: soco.discover(timeout=5))
        if discovered:
            for device in discovered:
                self._by_ip[device.ip_address] = device
                for name, info in reg.items():
                    if info.ip == device.ip_address:
                        self._devices[name] = device
                        break
                else:
                    # Speaker found but not in registry — add by Sonos name
                    try:
                        pname = await loop.run_in_executor(None, lambda d=device: d.player_name)
                        self._devices[pname] = device
                    except Exception:
                        pass

        # Direct IP fallback for registered speakers not found
        self._offline = []
        for name, info in reg.items():
            if name not in self._devices:
                try:
                    device = soco.SoCo(info.ip)
                    pname = await loop.run_in_executor(None, lambda d=device: d.player_name)
                    self._devices[name] = device
                    self._by_ip[info.ip] = device
                except Exception:
                    self._offline.append(name)

        self._last_discovery = time.time()

    async def ensure_fresh(self) -> None:
        """Re-discover if cache is stale."""
        if self.is_stale:
            await self.discover()

    def get(self, name: str) -> Optional[soco.SoCo]:
        """Get SoCo device by canonical speaker name."""
        return self._devices.get(name)

    def get_by_ip(self, ip: str) -> Optional[soco.SoCo]:
        return self._by_ip.get(ip)

    @property
    def online(self) -> Dict[str, soco.SoCo]:
        return dict(self._devices)

    @property
    def offline_names(self) -> List[str]:
        return list(self._offline)

    @property
    def all_names(self) -> List[str]:
        return list(self._devices.keys()) + self._offline
