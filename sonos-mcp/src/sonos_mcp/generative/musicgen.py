"""MusicGen local inference — Phase 3 stub."""

from typing import List
from .base import GenerativeMusicSource, GenerativeCapability, GenerativeRequest, GenerativeResult


class MusicGenSource(GenerativeMusicSource):
    """Meta MusicGen running on FX Mac (Phase 3).

    Planned: text prompt → local GPU inference → HTTP-served audio → Sonos play_uri()
    """

    @property
    def name(self) -> str:
        return "musicgen"

    @property
    def capabilities(self) -> List[GenerativeCapability]:
        return [
            GenerativeCapability.TEXT_TO_MUSIC,
            GenerativeCapability.CONTINUATION,
            GenerativeCapability.STYLE_TRANSFER,
        ]

    async def is_available(self) -> bool:
        return False  # Phase 3

    async def generate(self, request: GenerativeRequest) -> GenerativeResult:
        raise NotImplementedError("MusicGen not yet configured. Phase 3.")

    async def stop_generation(self) -> None:
        pass
