"""Mubert API integration — Phase 3 stub."""

from typing import List
from .base import GenerativeMusicSource, GenerativeCapability, GenerativeRequest, GenerativeResult


class MubertSource(GenerativeMusicSource):
    """Mubert real-time AI music streaming (Phase 3).

    Planned: mood/genre/BPM → HTTP stream URL → Sonos play_uri()
    """

    @property
    def name(self) -> str:
        return "mubert"

    @property
    def capabilities(self) -> List[GenerativeCapability]:
        return [GenerativeCapability.TEXT_TO_MUSIC, GenerativeCapability.AMBIENT]

    async def is_available(self) -> bool:
        return False  # Phase 3

    async def generate(self, request: GenerativeRequest) -> GenerativeResult:
        raise NotImplementedError("Mubert API not yet configured. Phase 3.")

    async def stop_generation(self) -> None:
        pass
