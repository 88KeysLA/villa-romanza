"""Amazon Music API integration — Phase 2 stub.

Will implement MusicService ABC using Amazon Music developer API
when API access is available.
"""

from typing import Optional
from .base import MusicService, SearchResult, BrowseResult


class AmazonMusicService(MusicService):
    """Amazon Music API integration (Phase 2).

    Planned features:
    - Search catalog (tracks, albums, playlists, stations)
    - Browse recommendations (personalized for-you)
    - Play items via Sonos (resolve to playable URI)
    - Playlist management
    """

    @property
    def name(self) -> str:
        return "amazon_music"

    @property
    def display_name(self) -> str:
        return "Amazon Music"

    async def is_available(self) -> bool:
        return False  # Phase 2

    async def search(self, query: str, category: Optional[str] = None,
                     limit: int = 20) -> SearchResult:
        raise NotImplementedError("Amazon Music API not yet configured. Phase 2.")

    async def browse(self, path: Optional[str] = None,
                     limit: int = 50) -> BrowseResult:
        raise NotImplementedError("Amazon Music API not yet configured. Phase 2.")

    async def get_playable_uri(self, item_id: str) -> Optional[str]:
        raise NotImplementedError("Amazon Music API not yet configured. Phase 2.")
