from pydantic import BaseModel
from enum import Enum


class Output(BaseModel):
    generated_by: str
    content: dict


class StrategyEnum(str, Enum):
    concrete = "concrete"


class Block(BaseModel):
    id: str
    name: str
    strategy: StrategyEnum
    metadata: dict
    upstream_block_ids: list[str]


def dfs_util(graph: dict[str, Block], key: str, color: dict):
    color[key] = "grey"
    for neighbour in graph[key].upstream_block_ids:
        if color[neighbour] == "grey":
            return True
        if color[neighbour] == "white":
            if dfs_util(graph, neighbour, color) == True:
                return True
    color[key] = "black"
    return False


def find_cycle(graph: dict) -> list[str]:
    color = {}
    for key in graph.keys():
        color[key] = "white"

    for key in graph.keys():
        if color[key] == "white":
            if dfs_util(graph, key, color) == True:
                return [item for item in color if color[item] == "grey"]
    return []


class Dag(BaseModel):
    name: str
    description: str
    task_definition: dict[str, Block]

    # run this validate when user post the DAG
    # if raised, return 400
    def validate(self):
        cycling_nodes = find_cycle(self.task_definition)
        if cycling_nodes:
            raise Exception(f"cycling at {cycling_nodes}")
