from pydantic import BaseModel
from enum import Enum


class Output(BaseModel):
    generated_by: str
    content: dict


class StrategyEnum(str, Enum):
    concrete = "concrete"


class Block(BaseModel):
    name: str
    strategy: StrategyEnum
    metadata: dict
    upstream_blocks: list[str]


class Dag(BaseModel):
    name: str
    description: str
    blocks: list[Block]
