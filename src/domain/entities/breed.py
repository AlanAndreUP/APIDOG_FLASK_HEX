from dataclasses import dataclass, field
from typing import Optional, List, Dict, Literal


@dataclass
class WeightRange:
    min: float
    max: float

    def __post_init__(self):
        if self.min > self.max:
            raise ValueError("WeightRange: 'min' cannot be greater than 'max'")


@dataclass
class LifeSpan:
    min: int
    max: int

    def __post_init__(self):
        if self.min > self.max:
            raise ValueError("LifeSpan: 'min' cannot be greater than 'max'")


@dataclass
class GroupRelationship:
    id: str
    type: Literal["group"] = "group"


@dataclass
class BreedAttributes:
    name: str
    description: Optional[str] = None
    life: Optional[LifeSpan] = None
    male_weight: Optional[WeightRange] = None
    female_weight: Optional[WeightRange] = None
    hypoallergenic: bool = False
   
   


@dataclass
class BreedRelationships:
    group: Optional[GroupRelationship] = None


@dataclass
class BreedLinks:
    self: str


@dataclass
class Breed:
    id: str
    attributes: BreedAttributes
    type: Literal["breed"] = "breed"
    relationships: Optional[BreedRelationships] = None
    links: Optional[BreedLinks] = None
    breed_group: Optional[str] = None
    image_url: Optional[str] = None
