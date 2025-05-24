from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class BreedReference:
    id: str
    type: str = "breed"


@dataclass
class GroupRelationships:
    breeds: Dict[str, List[BreedReference]] = field(default_factory=lambda: {"data": []})


@dataclass
class GroupAttributes:
    name: str


@dataclass
class Group:
    id: str
    attributes: GroupAttributes
    relationships: GroupRelationships = field(default_factory=GroupRelationships)
    type: str = "group" 