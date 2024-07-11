from abc import ABC, abstractmethod
from app.models import Output

class BaseStrategy(ABC):
    @abstractmethod
    def run(self, output_space: dict[str, Output]) -> Output:
        ...


class ConcreteStrategy(BaseStrategy):
    def __init__(self) -> None:
        super().__init__()

    def run(self, output_space: dict[str, Output]) -> Output:
        return super().run(output_space)
    
