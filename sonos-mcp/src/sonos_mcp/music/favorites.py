"""Sonos Favorites music service — browse and play saved favorites."""

import asyncio
from difflib import SequenceMatcher
from typing import Optional, List
from .base import MusicService, MusicItem, SearchResult, BrowseResult


class SonosFavoritesService(MusicService):
    """Access Sonos Favorites (may include Amazon Music, Spotify, etc. content)."""

    def __init__(self, get_any_device):
        """Args: get_any_device — callable returning any online SoCo device."""
        self._get_device = get_any_device

    @property
    def name(self) -> str:
        return "sonos_favorites"

    @property
    def display_name(self) -> str:
        return "Sonos Favorites"

    async def is_available(self) -> bool:
        try:
            device = self._get_device()
            return device is not None
        except Exception:
            return False

    async def _get_favorites(self) -> list:
        device = self._get_device()
        if not device:
            return []
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: list(device.get_sonos_favorites()))

    async def search(self, query: str, category: Optional[str] = None,
                     limit: int = 20) -> SearchResult:
        favs = await self._get_favorites()
        query_lower = query.lower()

        scored = []
        for fav in favs:
            title = getattr(fav, "title", "")
            score = SequenceMatcher(None, query_lower, title.lower()).ratio()
            if query_lower in title.lower():
                score = max(score, 0.9)
            scored.append((score, fav))

        scored.sort(key=lambda x: x[0], reverse=True)
        items = [self._to_item(fav) for _, fav in scored[:limit]]

        return SearchResult(
            items=items, total_matches=len(scored),
            query=query, service_name=self.name,
        )

    async def browse(self, path: Optional[str] = None,
                     limit: int = 50) -> BrowseResult:
        favs = await self._get_favorites()
        items = [self._to_item(fav) for fav in favs[:limit]]
        return BrowseResult(items=items, path="root", service_name=self.name)

    async def get_playable_uri(self, item_id: str) -> Optional[str]:
        favs = await self._get_favorites()
        for fav in favs:
            if getattr(fav, "item_id", None) == item_id:
                if fav.resources:
                    return fav.resources[0].uri
        return None

    def _to_item(self, fav) -> MusicItem:
        uri = fav.resources[0].uri if fav.resources else None
        return MusicItem(
            item_id=getattr(fav, "item_id", ""),
            title=getattr(fav, "title", "Unknown"),
            item_type="favorite",
            album_art_uri=getattr(fav, "album_art_uri", None),
            uri=uri,
            service_name=self.name,
        )
