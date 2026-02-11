"""Abstract base for music service integrations."""

from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class MusicItem(BaseModel):
    """Universal music item representation."""
    item_id: str
    title: str
    item_type: str  # "track", "album", "playlist", "station", "favorite"
    artist: Optional[str] = None
    album: Optional[str] = None
    album_art_uri: Optional[str] = None
    uri: Optional[str] = None
    duration_seconds: Optional[int] = None
    service_name: str
    metadata: dict = {}


class SearchResult(BaseModel):
    items: List[MusicItem]
    total_matches: int
    query: str
    service_name: str


class BrowseResult(BaseModel):
    items: List[MusicItem]
    path: str
    service_name: str


class MusicService(ABC):
    """Abstract interface for all music sources.

    Phase 1: SonosFavoritesService, TuneInService
    Phase 2: AmazonMusicService
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def display_name(self) -> str: ...

    @abstractmethod
    async def is_available(self) -> bool: ...

    @abstractmethod
    async def search(self, query: str, category: Optional[str] = None,
                     limit: int = 20) -> SearchResult: ...

    @abstractmethod
    async def browse(self, path: Optional[str] = None,
                     limit: int = 50) -> BrowseResult: ...

    @abstractmethod
    async def get_playable_uri(self, item_id: str) -> Optional[str]: ...
