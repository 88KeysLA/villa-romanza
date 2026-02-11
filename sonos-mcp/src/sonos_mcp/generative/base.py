"""Abstract base for generative music sources — Phase 3 scaffold."""

from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class GenerativeCapability(str, Enum):
    TEXT_TO_MUSIC = "text_to_music"
    STYLE_TRANSFER = "style_transfer"
    CONTINUATION = "continuation"
    AMBIENT = "ambient"


class GenerativeRequest(BaseModel):
    prompt: str
    duration_seconds: int = 30
    style: Optional[str] = None
    bpm: Optional[int] = None
    energy: Optional[float] = None  # 0.0-1.0


class GenerativeResult(BaseModel):
    stream_uri: str  # HTTP URI playable by Sonos
    duration_seconds: int
    generator_name: str
    prompt: str
    metadata: dict = {}


class GenerativeMusicSource(ABC):
    """Abstract interface for generative music engines.

    Phase 3: MubertSource (cloud API), MusicGenSource (local GPU inference)
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def capabilities(self) -> List[GenerativeCapability]: ...

    @abstractmethod
    async def is_available(self) -> bool: ...

    @abstractmethod
    async def generate(self, request: GenerativeRequest) -> GenerativeResult: ...

    @abstractmethod
    async def stop_generation(self) -> None: ...
