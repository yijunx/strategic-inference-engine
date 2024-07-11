from app.strategy import ConcreteStrategy, BaseStrategy
from app.models import Dag, StrategyEnum, Block, Output


strategy_enum_to_strategy_mapping: dict[StrategyEnum, BaseStrategy] = {
    StrategyEnum.concrete: ConcreteStrategy(
        # here you may init with openai keys
    )
}


def plan(dag: Dag) -> list[Block]:
    block_dict = {}
    queue = []
    while len(queue) < len(dag.blocks):
        added = 0
        for block in dag.blocks:
            if block.name in block_dict:
                # we have arranged this guy
                ...
            else:
                if block.upstream_blocks:
                    can_add = True
                    for upstream_block_name in block.upstream_blocks:
                        if upstream_block_name in block_dict:
                            ...
                        else:
                            can_add = False
                    if can_add:
                        added + 1
                        queue.append(block)
                        block_dict[block.name] = block
                else:
                    # no upstream, just add
                    added += 1
                    queue.append(block)
                    block_dict[block.name] = block
        if added == 0:
            # nothing changes ths round
            break
    return queue


def execute(queue: list[Block]) -> Output:
    output_space = {}
    for block in queue:
        s = strategy_enum_to_strategy_mapping[block.strategy]
        s.run(output_space=output_space)
    return output_space[queue[-1].name]


def process_dag(dag: Dag) -> Output:
    queue = plan(dag)
    return execute(queue)

