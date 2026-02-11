"""Speaker registry, zone definitions, and constants for Villa Romanza."""

from pydantic import BaseModel
from typing import List, Dict

# Safety
VOLUME_HARD_MAX = 70  # Constitution Section B.2
VOLUME_DEFAULT = 25
CHARACTER_LIMIT = 25000

# Timeouts
SOCO_TIMEOUT = 10.0
HA_TIMEOUT = 10.0
DISCOVERY_CACHE_TTL = 300  # 5 minutes


class SpeakerInfo(BaseModel):
    """Static speaker registry entry."""
    name: str
    ip: str
    ha_entity: str
    network_name: str
    room: str
    aliases: List[str] = []


class ZoneDefinition(BaseModel):
    """A logical zone grouping speakers."""
    zone_id: str
    display_name: str
    speakers: List[str]
    default_coordinator: str
    description: str = ""
    max_volume: int = VOLUME_HARD_MAX


# --- Speaker Registry (from fixed_ip_reservations.md) ---
SPEAKERS: Dict[str, SpeakerInfo] = {
    "Library": SpeakerInfo(
        name="Library", ip="192.168.0.100", ha_entity="media_player.library",
        network_name="SNS-Library", room="Library",
        aliases=["lib", "reading room"],
    ),
    "Lounge": SpeakerInfo(
        name="Lounge", ip="192.168.0.101", ha_entity="media_player.lounge",
        network_name="SNS-Lounge", room="Lounge",
        aliases=["living room", "great room", "soggiorno"],
    ),
    "Kitchen": SpeakerInfo(
        name="Kitchen", ip="192.168.0.102", ha_entity="media_player.kitchen",
        network_name="SNS-Kitchen", room="Kitchen",
        aliases=["cucina"],
    ),
    "Dining": SpeakerInfo(
        name="Dining", ip="192.168.0.103", ha_entity="media_player.dining",
        network_name="SNS-Dining", room="Dining",
        aliases=["dining room"],
    ),
    "Entrata": SpeakerInfo(
        name="Entrata", ip="192.168.0.104", ha_entity="media_player.entrata",
        network_name="SNS-Entrata", room="Entrata",
        aliases=["entry", "entrance", "foyer"],
    ),
    "Hers": SpeakerInfo(
        name="Hers", ip="192.168.0.105", ha_entity="media_player.hers",
        network_name="SNS-Hers", room="Hers",
        aliases=["her room", "her bath", "her bathroom"],
    ),
    "Master Entry": SpeakerInfo(
        name="Master Entry", ip="192.168.0.106", ha_entity="media_player.master_entry",
        network_name="SNS-MasterEntry", room="Master Entry",
        aliases=["master entrance", "master hall"],
    ),
    "His": SpeakerInfo(
        name="His", ip="192.168.0.107", ha_entity="media_player.his",
        network_name="SNS-His", room="His",
        aliases=["his room", "his bath", "his bathroom"],
    ),
    "Blue Bedroom": SpeakerInfo(
        name="Blue Bedroom", ip="192.168.0.109", ha_entity="media_player.blue_bedroom",
        network_name="SNS-BlueBedroom", room="Blue Bedroom",
        aliases=["blue room", "blue"],
    ),
    "Pink Bedroom": SpeakerInfo(
        name="Pink Bedroom", ip="192.168.0.110", ha_entity="media_player.pink_bedroom",
        network_name="SNS-PinkBedroom", room="Pink Bedroom",
        aliases=["pink room", "pink", "mads room"],
    ),
    "Up Guest": SpeakerInfo(
        name="Up Guest", ip="192.168.0.111", ha_entity="media_player.up_guest",
        network_name="SNS-GuestUp", room="Up Guest",
        aliases=["upper guest", "guest up", "upstairs guest"],
    ),
    "Down Guest": SpeakerInfo(
        name="Down Guest", ip="192.168.0.112", ha_entity="media_player.down_guest",
        network_name="SNS-GuestDown", room="Down Guest",
        aliases=["lower guest", "guest down", "downstairs guest"],
    ),
    "Garage": SpeakerInfo(
        name="Garage", ip="192.168.0.113", ha_entity="media_player.garage",
        network_name="SNS-Garage", room="Garage",
        aliases=[],
    ),
    "Wine": SpeakerInfo(
        name="Wine", ip="192.168.0.114", ha_entity="media_player.wine",
        network_name="SNS-Wine", room="Wine Cellar",
        aliases=["wine cellar", "cellar", "cava"],
    ),
    "Porch": SpeakerInfo(
        name="Porch", ip="192.168.0.115", ha_entity="media_player.porch",
        network_name="SNS-Porch", room="Porch",
        aliases=["front porch", "veranda"],
    ),
    "Lawn": SpeakerInfo(
        name="Lawn", ip="192.168.0.116", ha_entity="media_player.lawn",
        network_name="SNS-Lawn", room="Lawn",
        aliases=["garden", "yard"],
    ),
    "Picnic": SpeakerInfo(
        name="Picnic", ip="192.168.0.117", ha_entity="media_player.picnic",
        network_name="SNS-Picnic", room="Picnic",
        aliases=["picnic area"],
    ),
    "Pool North": SpeakerInfo(
        name="Pool North", ip="192.168.0.118", ha_entity="media_player.pool_north",
        network_name="SNS-PoolNorth", room="Pool",
        aliases=["pool n"],
    ),
    "Pool South": SpeakerInfo(
        name="Pool South", ip="192.168.0.119", ha_entity="media_player.pool_south",
        network_name="SNS-PoolSouth", room="Pool",
        aliases=["pool s"],
    ),
    "Pool East": SpeakerInfo(
        name="Pool East", ip="192.168.0.121", ha_entity="media_player.pool_east",
        network_name="SNS-PoolEast", room="Pool",
        aliases=["pool e"],
    ),
    "Cabana": SpeakerInfo(
        name="Cabana", ip="192.168.0.120", ha_entity="media_player.cabana",
        network_name="SNS-Cabana", room="Cabana",
        aliases=["pool house"],
    ),
    "Bar": SpeakerInfo(
        name="Bar", ip="192.168.0.122", ha_entity="media_player.bar",
        network_name="SNS-PT-Bar", room="Bar",
        aliases=["bar theatre", "theatre"],
    ),
    "Bar Surround": SpeakerInfo(
        name="Bar Surround", ip="192.168.0.123", ha_entity="media_player.bar_from",
        network_name="SNS-PT-SyncFeed", room="Bar",
        aliases=["bar from", "bar to", "surround"],
    ),
    "Sunroom Soundbar": SpeakerInfo(
        name="Sunroom Soundbar", ip="192.168.0.124",
        ha_entity="media_player.ambeo_sunroom_soundbar",
        network_name="SNS-PT-Sunroom", room="Sun Room",
        aliases=["sunroom", "sun room", "ambeo"],
    ),
    "Picnic Sub": SpeakerInfo(
        name="Picnic Sub", ip="192.168.0.125", ha_entity="media_player.lawn_sub_2",
        network_name="SNS-PicnicSub", room="Picnic",
        aliases=["sub", "subwoofer", "lawn sub"],
    ),
}

# HA-only speakers (no fixed IP in reservations, discovered via SoCo)
HA_ONLY_SPEAKERS = {
    "Master Bed": "media_player.master_bed",
    "Master Send": "media_player.master_send",
    "M Rear": "media_player.m_rear",
    "Master": "media_player.master",
}

# --- Zone Definitions ---
ZONES: Dict[str, ZoneDefinition] = {
    "great_room": ZoneDefinition(
        zone_id="great_room", display_name="Great Room",
        speakers=["Lounge", "Kitchen", "Dining", "Library"],
        default_coordinator="Lounge",
        description="Main living area open-plan speakers",
    ),
    "master_suite": ZoneDefinition(
        zone_id="master_suite", display_name="Master Suite",
        speakers=["Master Bed", "Master Entry", "His", "Hers", "Master Send", "M Rear"],
        default_coordinator="Master Bed",
        description="Master bedroom and ensuite",
    ),
    "pool": ZoneDefinition(
        zone_id="pool", display_name="Pool Area",
        speakers=["Pool North", "Pool South", "Pool East", "Cabana"],
        default_coordinator="Pool North",
        description="Pool deck and cabana",
    ),
    "outdoor": ZoneDefinition(
        zone_id="outdoor", display_name="Outdoor",
        speakers=["Lawn", "Picnic", "Pool North", "Pool South", "Pool East", "Cabana"],
        default_coordinator="Lawn",
        description="All outdoor speakers",
    ),
    "bedrooms": ZoneDefinition(
        zone_id="bedrooms", display_name="Bedrooms",
        speakers=["Blue Bedroom", "Pink Bedroom", "Up Guest", "Down Guest"],
        default_coordinator="Blue Bedroom",
        description="Guest bedrooms",
    ),
    "bar": ZoneDefinition(
        zone_id="bar", display_name="Bar & Theatre",
        speakers=["Bar", "Bar Surround"],
        default_coordinator="Bar",
        description="Bar area with Anthem surround",
    ),
    "entertain": ZoneDefinition(
        zone_id="entertain", display_name="Entertainment",
        speakers=["Lounge", "Kitchen", "Dining", "Library", "Entrata", "Wine", "Bar"],
        default_coordinator="Lounge",
        description="Full indoor entertainment zone",
    ),
    "whole_house": ZoneDefinition(
        zone_id="whole_house", display_name="Whole House",
        speakers=["ALL"],
        default_coordinator="Lounge",
        description="Every speaker (party mode)",
    ),
}
