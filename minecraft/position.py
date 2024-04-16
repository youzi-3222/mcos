"""
坐标。
"""

from typing import Union


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

    def delta(self, delta_x: float, delta_y: float, delta_z: float):
        """
        位移。
        """
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z
        return self


class AxisPosition:
    """
    坐标轴上坐标信息。
    """

    relative: bool = False
    """是否是相对坐标。"""
    _value: float = 0.0
    """坐标轴值。"""

    def __init__(self, value: Union[float, str]) -> None:
        if isinstance(value, str):
            if value.startswith("~"):
                self.relative = True
                self._value = float(value[1:])
            else:
                self._value = float(value)
        else:
            self._value = value

    def value(self, base: float):
        """
        获取值。
        """
        return self._value + (base if self.relative else 0)


class RelativePosition:
    """
    相对坐标信息（未完成）。
    """

    x: AxisPosition
    """X 坐标。"""
    y: AxisPosition
    """Y 坐标。"""
    z: AxisPosition
    """Z 坐标。"""

    def __init__(self, x: Union[float, str], y: float, z: float) -> None:
        self.x = AxisPosition(x)
        self.y = AxisPosition(y)
        self.z = AxisPosition(z)

    def list(self, base: Position):
        """
        获取 `[x, y, z]`。
        """
        return [self.x.value(base.x), self.y.value(base.y), self.z.value(base.z)]
