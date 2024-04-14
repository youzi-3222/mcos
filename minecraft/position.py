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

    @property
    def list(self):
        """
        获取 `[x, y, z]`。
        """
        return [self.x, self.y, self.z]
