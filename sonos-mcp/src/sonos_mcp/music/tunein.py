"""TuneIn radio service via SoCo — search and play radio stations."""

import asyncio
from typing import Optional
from .base import MusicService, MusicItem, SearchResult, BrowseResult


class TuneInService(MusicService):
    """Search and play TuneIn radio stations through Sonos."""

    def __init__(self, get_any_device):
        self._get_device = get_any_device
        self._soco_service = None

    @property
    def name(self) -> str:
        return "tunein"

    @property
    def display_name(self) -> str:
        return "TuneIn Radio"

    async def _ensure_service(self):
        if self._soco_service is None:
            loop = asyncio.get_event_loop()
            from soco.music_services import MusicService as SocoMS
            self._soco_service = await loop.run_in_executor(None, lambda: SocoMS("TuneIn"))

    async def is_available(self) -> bool:
        try:
            await self._ensure_service()
            return True
        except Exception:
            return False

    async def search(self, query: str, category: Optional[str] = None,
                     limit: int = 20) -> SearchResult:
        await self._ensure_service()
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                None, lambda: self._soco_service.search("stations", query, count=limit)
            )
            items = []
            for item in result:
                items.append(MusicItem(
                    item_id=getattr(item, "item_id", ""),
                    title=getattr(item, "title", "Unknown"),
                    item_type="station",
                    album_art_uri=getattr(item, "album_art_uri", None),
                    service_name=self.name,
                ))
            return SearchResult(
                items=items, total_matches=len(items),
                query=query, service_name=self.name,
            )
        except Exception as e:
            return SearchResult(
                items=[], total_matches=0,
                query=query, service_name=self.name,
            )

    async def browse(self, path: Optional[str] = None,
                     limit: int = 50) -> BrowseResult:
        await self._ensure_service()
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                None, lambda: self._soco_service.get_metadata(item=path, count=limit)
            )
            items = [MusicItem(
                item_id=getattr(item, "item_id", ""),
                title=getattr(item, "title", "Unknown"),
                item_type="station",
                service_name=self.name,
            ) for item in result]
            return BrowseResult(items=items, path=path or "root", service_name=self.name)
        except Exception:
            return BrowseResult(items=[], path=path or "root", service_name=self.name)

    async def get_playable_uri(self, item_id: str) -> Optional[str]:
        await self._ensure_service()
        loop = asyncio.get_event_loop()
        try:
            uri = await loop.run_in_executor(
                None, lambda: self._soco_service.sonos_uri_from_id(item_id)
            )
            return uri
        except Exception:
            return None
