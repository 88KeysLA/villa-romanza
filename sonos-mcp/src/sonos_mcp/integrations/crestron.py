"""Crestron state awareness — Phase 2 stub."""

from typing import Optional, Dict, Any


class CrestronAwareness:
    """Read-only Crestron state for AV context.

    Phase 1: All methods return None/empty (stub).
    Phase 2: Connects to CP4-R REST API to read source selections.
    """

    def __init__(self, host: Optional[str] = None, auth_token: Optional[str] = None):
        self.host = host
        self.auth_token = auth_token

    async def get_room_source(self, room_name: str) -> Optional[str]:
        return None  # Phase 2

    async def get_active_media_zones(self) -> Dict[str, Any]:
        return {}  # Phase 2

    async def is_room_watching(self, room_name: str) -> bool:
        return False  # Phase 2
