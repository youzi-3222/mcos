"""
将区域内方块分割为小块。
"""

from minecraft.block.range import BlockRange
from minecraft.position import Position


def split(block_range: BlockRange, max_split: int = 8):
    """
    将区域内方块分割成小块。
    """
    for x in range(round(block_range.p1.x), round(block_range.p2.x) + 1, max_split):
        for y in range(round(block_range.p1.y), round(block_range.p2.y) + 1, max_split):
            for z in range(
                round(block_range.p1.z), round(block_range.p2.z) + 1, max_split
            ):
                yield BlockRange(
                    Position(x, y, z),
                    Position(
                        min(block_range.p2.x, x + max_split - 1),
                        min(block_range.p2.y, y + max_split - 1),
                        min(block_range.p2.z, z + max_split - 1),
                    ),
                )
