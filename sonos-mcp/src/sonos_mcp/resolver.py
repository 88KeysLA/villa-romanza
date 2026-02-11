"""Fuzzy speaker and zone name resolution for natural language input."""

from difflib import SequenceMatcher
from typing import Optional, List, Union
from pydantic import BaseModel
from .config import SPEAKERS, ZONES, SpeakerInfo, ZoneDefinition


class ResolveResult(BaseModel):
    """Result of speaker/zone resolution."""
    resolved: bool
    match_type: Optional[str] = None  # "speaker" or "zone"
    speaker_name: Optional[str] = None
    zone_id: Optional[str] = None
    confidence: float = 0.0
    candidates: List[dict] = []


# Special tokens that map to whole_house zone
PARTY_TOKENS = {"everywhere", "all", "all speakers", "whole house", "party", "party mode"}


class SpeakerResolver:
    """Resolves natural language to speakers or zones."""

    def resolve(self, utterance: str) -> ResolveResult:
        utterance_lower = utterance.strip().lower()

        # Special tokens
        if utterance_lower in PARTY_TOKENS:
            return ResolveResult(
                resolved=True, match_type="zone",
                zone_id="whole_house", confidence=1.0,
            )

        # 1. Exact match on speaker canonical names
        for name in SPEAKERS:
            if utterance_lower == name.lower():
                return ResolveResult(
                    resolved=True, match_type="speaker",
                    speaker_name=name, confidence=1.0,
                )

        # 2. Exact match on zone display names / zone_ids
        for zid, zone in ZONES.items():
            if utterance_lower in (zid.lower(), zone.display_name.lower()):
                return ResolveResult(
                    resolved=True, match_type="zone",
                    zone_id=zid, confidence=1.0,
                )

        # 3. Fuzzy match against speaker names + aliases
        best_speaker = None
        best_speaker_score = 0.0
        for name, info in SPEAKERS.items():
            candidates_for_name = [name.lower()] + [a.lower() for a in info.aliases]
            candidates_for_name.append(info.room.lower())
            for candidate in candidates_for_name:
                score = SequenceMatcher(None, utterance_lower, candidate).ratio()
                # Bonus if candidate is contained in utterance
                if candidate in utterance_lower:
                    score = max(score, 0.85)
                if utterance_lower in candidate:
                    score = max(score, 0.80)
                if score > best_speaker_score:
                    best_speaker_score = score
                    best_speaker = name

        # 4. Fuzzy match against zone names
        best_zone = None
        best_zone_score = 0.0
        for zid, zone in ZONES.items():
            candidates_for_zone = [zid.lower(), zone.display_name.lower()]
            for candidate in candidates_for_zone:
                score = SequenceMatcher(None, utterance_lower, candidate).ratio()
                if candidate in utterance_lower:
                    score = max(score, 0.85)
                if score > best_zone_score:
                    best_zone_score = score
                    best_zone = zid

        # Pick the best overall match
        if best_speaker_score >= best_zone_score and best_speaker_score >= 0.6:
            return ResolveResult(
                resolved=best_speaker_score >= 0.7,
                match_type="speaker",
                speaker_name=best_speaker,
                confidence=best_speaker_score,
                candidates=self._get_candidates(utterance_lower) if best_speaker_score < 0.7 else [],
            )
        elif best_zone_score >= 0.6:
            return ResolveResult(
                resolved=best_zone_score >= 0.7,
                match_type="zone",
                zone_id=best_zone,
                confidence=best_zone_score,
                candidates=self._get_candidates(utterance_lower) if best_zone_score < 0.7 else [],
            )

        # No good match
        return ResolveResult(
            resolved=False,
            confidence=max(best_speaker_score, best_zone_score),
            candidates=self._get_candidates(utterance_lower),
        )

    def _get_candidates(self, utterance: str, top_n: int = 5) -> List[dict]:
        """Return top-N candidates sorted by score."""
        results = []
        for name, info in SPEAKERS.items():
            score = max(
                SequenceMatcher(None, utterance, name.lower()).ratio(),
                *(SequenceMatcher(None, utterance, a.lower()).ratio() for a in info.aliases)
                if info.aliases else [0.0],
            )
            results.append({"type": "speaker", "name": name, "score": round(score, 2)})
        for zid, zone in ZONES.items():
            score = SequenceMatcher(None, utterance, zone.display_name.lower()).ratio()
            results.append({"type": "zone", "name": zone.display_name, "id": zid, "score": round(score, 2)})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]
