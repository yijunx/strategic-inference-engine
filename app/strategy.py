from abc import ABC, abstractmethod
from app.models import Output, Block


class BaseStrategy(ABC):
    @abstractmethod
    def run(self, output_space: dict[str, Output]) -> Output: ...


class ConcreteStrategy(BaseStrategy):
    def __init__(self, block: Block) -> None:
        self.block = block
        # get the openai endpont here

    async def run(self, output_space: dict[str, Output]) -> None:
        # use the async stuff for openai endpoinds
        output_space[self.block.name] = Output()
        # also report your process somewhere!!!
        # like a notification api
