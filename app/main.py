from app.strategy import ConcreteStrategy, BaseStrategy
from app.models import Dag, StrategyEnum, Block, Output
import asyncio

strategy_enum_to_strategy_mapping: dict[StrategyEnum, BaseStrategy] = {
    StrategyEnum.concrete: ConcreteStrategy(
        # here you may init with openai keys
        # or other stuff
    )
}


def plan(dag: Dag) -> list[list[Block]]:
    block_dict = {}
    queue = []
    while len(queue) < len(dag.task_definition):
        batch_block = []
        for b_id, block in dag.task_definition.items():
            if b_id in block_dict:
                # we have arranged this guy
                ...
            else:
                if block.upstream_block_ids:
                    can_add = True
                    for upstream_block_id in block.upstream_block_ids:
                        if upstream_block_id in block_dict:
                            ...
                        else:
                            can_add = False
                    if can_add:
                        batch_block.append(block)
                        block_dict[block.id] = block
                else:
                    # no upstream, just add
                    batch_block.append(block)
                    block_dict[block.id] = block
        if len(batch_block) == 0:
            # nothing changes ths round
            break
        else:
            queue.append(batch_block)
    return queue


async def execute_strategies(
    output_space: dict, strategies: list[BaseStrategy]
) -> None:
    await asyncio.gather(*[s.run(output_space) for s in strategies])


def execute(queue: list[list[Block]]) -> Output:
    output_space = {}
    for batch_block in queue:
        strategies = [
            strategy_enum_to_strategy_mapping[block.strategy] for block in batch_block
        ]
        # here use acync io
        asyncio.run(
            execute_strategies(output_space=output_space, strategies=strategies)
        )
    # last layer block has to be only one, to be our only output
    # actually return here is not important
    # we should send notification throughout the execution
    return output_space[queue[-1][0].name]


def process_dag(dag: Dag) -> Output:
    queue = plan(dag)
    return execute(queue)
