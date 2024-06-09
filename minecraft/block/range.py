"""
方块区域。
"""

from minecraft.position import Position


class BlockRange:
    """
    一个区域内方块的集合。

    保证 `p1` 的每个坐标值总小于（等于）`p2`。
    """

    p1: Position
    p2: Position

    def __init__(self, pos1: Position, pos2: Position) -> None:
        self.p1 = Position(
            min(pos1.x, pos2.x), min(pos1.y, pos2.y), min(pos1.z, pos2.z)
        )
        self.p2 = Position(
            max(pos1.x, pos2.x), max(pos1.y, pos2.y), max(pos1.z, pos2.z)
        )

    def __iter__(self):
        return (x for x in [*self.p1, *self.p2])

    @property
    def delta_x(self) -> float:
        """
        X 坐标的差值。
        """
        return self.p2.x - self.p1.x

    @property
    def delta_y(self) -> float:
        """
        Y 坐标的差值。
        """
        return self.p2.y - self.p1.y

    @property
    def delta_z(self) -> float:
        """
        Z 坐标的差值。
        """
        return self.p2.z - self.p1.z
