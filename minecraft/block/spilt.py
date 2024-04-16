"""
将区域内方块分割为小块。
"""

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

    def __iter__(self):
        for x in range(round(self.p1.x), round(self.p2.x), self.max_spilt):
            for y in range(round(self.p1.y), round(self.p2.y), self.max_spilt):
                for z in range(round(self.p1.z), round(self.p2.z), self.max_spilt):
                    yield BlockRange(
                        Position(x, y, z),
                        Position(
                            min(self.p2.x, x + self.max_spilt - 1),
                            min(self.p2.y, y + self.max_spilt - 1),
                            min(self.p2.z, z + self.max_spilt - 1),
                        ),
                    )
