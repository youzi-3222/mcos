"""
坐标。
"""


class Position:
    """
    坐标信息。
    """

    x: float = 0.0
    """X 坐标。"""
    y: float = 0.0
    """Y 坐标。"""
    z: float = 0.0
    """Z 坐标。"""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return (x for x in [self.x, self.y, self.z])

    def __str__(self):
        return f"Position({self.x}, {self.y}, {self.z})"

    def delta(self, delta_x: float, delta_y: float, delta_z: float):
        """
        位移。返回新的对象实例（而非直接操作）！
        """
        return Position(self.x + delta_x, self.y + delta_y, self.z + delta_z)
