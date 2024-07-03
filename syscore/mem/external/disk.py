"""
硬盘。
"""

import math
from minecraft.block.range import BlockRange
from minecraft.position import Position
from minecraft.world import world
from syscore.mem.external.blocks import encode_data, decode_data
from syscore.mem.external.coding import bytes2digits, digits2bytes


class Disk(BlockRange):
    """
    硬盘。

    读写顺序：Y-X-Z，以避免多次 tp 玩家加载区块。

    `p1` `p2` 属性指示其实际可用的空间（而非外壳顶点坐标）。
    """

    _loc: int

    @property
    def loc(self) -> int:
        """磁头指针位置。"""
        return self._loc

    @loc.setter
    def loc(self, new: int):
        """设置磁头指针位置。"""
        self._loc = new

    @property
    def loc_pos(self) -> Position:
        """
        磁头指针指向的方块。
        """
        return self.p1.delta(
            self.loc % self.delta_x,
            (self.loc // self.delta_x) % self.delta_y,
            self.loc // (self.delta_x * self.delta_y),
        )

    @property
    def size(self) -> int:
        """大小，单位为比特（8 位）。"""
        return math.floor(
            round(self.delta_x) * round(self.delta_y) * round(self.delta_z) * 0.625
        )

    def generate_shell(self):
        """
        生成外壳。
        """
        world.fill(
            BlockRange(self.p1.delta(-2, -2, -2), self.p2.delta(2, 2, 2)),
            block=251,  # 混凝土
            data=8,
            hollow=True,
        )
        world.fill(
            BlockRange(self.p1.delta(-1, -1, -1), self.p2.delta(1, 1, 1)),
            block=49,  # 黑曜石
            hollow=True,
        )

    def read(self, length: int) -> bytes:
        """
        读取。
        """
        blocks = []
        for _ in range(length):
            blocks.append(world.get(self.loc_pos))
            self.loc += 1
        return digits2bytes(decode_data(blocks))

    def write(self, data: bytes):
        """
        写入。
        """
        blocks = encode_data(bytes2digits(data))
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 1

    def format(self):
        """
        格式化（未完成）。
        """
        raise NotImplementedError
