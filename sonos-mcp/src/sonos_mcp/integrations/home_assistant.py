"""Lightweight HA REST API client for reading villa state."""

import httpx
from typing import Optional, Dict, Any


class HomeAssistantClient:
    """Reads HA state via REST API to enforce constitution constraints."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._client: Optional[httpx.AsyncClient] = None

    async def initialize(self):
        self._client = httpx.AsyncClient(
            base_url=f"{self.base_url}/api",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(10.0),
            verify=True,
        )

    async def close(self):
        if self._client:
            await self._client.aclose()

    async def get_state(self, entity_id: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/states/{entity_id}")
        resp.raise_for_status()
        return resp.json()

    async def get_villa_mode(self) -> str:
        """Returns: NORMAL, LISTEN, WATCH, ENTERTAIN, LIVE_JAM, SHOW, INTERLUDE"""
        state = await self.get_state("input_select.villa_mode")
        return state["state"]

    async def is_agent_media_enabled(self) -> bool:
        state = await self.get_state("input_boolean.agent_controlled_media_enable")
        return state["state"] == "on"

    async def get_autonomy_phase(self) -> str:
        state = await self.get_state("input_select.agent_controlled_autonomy_phase")
        return state["state"]


async def check_agent_media_gate(ha_client: Optional[HomeAssistantClient]) -> None:
    """Raises ValueError if agent media control is not enabled.
    Skips check if HA client is not configured (allows standalone testing).
    """
    if ha_client is None:
        return
    try:
        if not await ha_client.is_agent_media_enabled():
            raise ValueError(
                "Agent media control is disabled. "
                "Enable input_boolean.agent_controlled_media_enable in HA first."
            )
    except httpx.HTTPError:
        pass  # HA unreachable — allow operation (fail-open for manual use)
