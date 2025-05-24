from dataclasses import dataclass, field


@dataclass
class FactAttributes:
    body: str


@dataclass
class Fact:
    id: str
    attributes: FactAttributes
    type: str = "fact" 
