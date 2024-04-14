"""
将区域内方块分割为小块。
"""

from typing import Any, Generator
from minecraft.block.range import BlockRange
from minecraft.position import Position


class SpiltBlockRange(BlockRange):
    """
    一个区域内方块的集合。

    保证 `p1` 的每个坐标值总小于（等于）`p2`。

    提供分割方块功能。
    """

    def __init__(self, pos1: Position, pos2: Position, max_spilt: int = 8) -> None:
        super().__init__(pos1, pos2)
        self.max_spilt = max_spilt

    def __iter__(self) -> Generator[BlockRange, Any, None]:
        for x in range(int(self.delta_x // self.max_spilt + 1)):
            for y in range(int(self.delta_y // self.max_spilt + 1)):
                for z in range(int(self.delta_z // self.max_spilt + 1)):
                    yield BlockRange(
                        Position(x, y, z),
                        Position(
                            x + self.max_spilt, y + self.max_spilt, z + self.max_spilt
                        ),
                    )
