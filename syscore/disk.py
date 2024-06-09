"""
硬盘。
"""

from minecraft.block.range import BlockRange
from minecraft.position import Position
from minecraft.world import world


class Disk(BlockRange):
    """
    硬盘。
    """

    _location: int

    @property
    def location(self) -> int:
        """（磁头）指针位置。"""
        return self._location

    def generate_shell(self):
        """
        生成外壳。
        """
        world.fill(
            BlockRange(self.p1.delta(-2, -2, -2), self.p2.delta(2, 2, 2)),
            block=251,
            data=8,
            hollow=True,
        )
        world.fill(
            BlockRange(self.p1.delta(-1, -1, -1), self.p2.delta(1, 1, 1)),
            block=49,
            hollow=True,
        )

    def format(self):
        """
        格式化。
        """
        raise NotImplementedError
