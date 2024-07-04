"""
硬盘。
"""

import math
from minecraft.block.range import BlockRange
from minecraft.position import Position
from minecraft.world import world
from syscore.mem.external.blocks import encode_data, decode_data
from syscore.mem.external.coding import bytes2digits, digits2bytes

VERSION_CODE = 1
"""
版本号。
"""


class Disk(BlockRange):
    """
    硬盘。

    读写顺序：Y-X-Z，以避免多次 tp 玩家加载区块。

    `p1` `p2` 属性指示其实际可用的空间（而非外壳顶点坐标）。
    """

    _loc: int = 0

    @property
    def loc(self) -> int:
        """磁头指针位置。"""
        return self._loc

    @loc.setter
    def loc(self, new: int):
        """设置磁头指针位置。"""
        if not 0 <= new < self.size:
            raise ValueError(f"{new} is out of range [0,{self.size})")
        self._loc = new

    @property
    def loc_pos(self) -> Position:
        """
        磁头指针指向的方块。
        """
        return self.p1.delta(
            (self.loc // self.delta_y) % self.delta_x,
            (self.loc) % self.delta_y,
            self.loc // (self.delta_x * self.delta_y),
        )

    @property
    def bit(self) -> int:
        """大小，单位为比特（8 位）。"""
        return math.floor(
            round(self.delta_x) * round(self.delta_y) * round(self.delta_z) * 0.625
        )

    @property
    def size(self) -> int:
        """大小，单位为五位二进制。"""
        return round(self.delta_x) * round(self.delta_y) * round(self.delta_z)

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

    def write(self, data: bytes, length: bool = False):
        """
        写入。

        ### 参数
        - `length`：是否在数据之前写入长度。
        """
        blocks = encode_data(bytes2digits(data))
        if length:
            blocks = encode_data(bytes2digits(bytes(len(blocks)) + b";" + data))
        if (len(blocks) + self.loc) >= self.size:
            raise ValueError(
                f"Out of range: at {self.loc}, write {len(blocks)}, size {self.size}"
            )
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 1

    def _clear(self):
        """
        清空。
        """
        try:
            self.loc = 0
            while True:
                self.write(b"\x00")
        except ValueError:
            self.loc = 0
            return True
        except:
            self.loc = 0
            return False

    def format(self, logical: int = 1024):
        """
        格式化（未完成）。

        ### 参数
        - `logical`：每个逻辑块的大小，单位为五位二进制（个方块）。
        """
        self._clear()
        self.loc = 0
        super_info = ""
        super_info += hex(VERSION_CODE)[2:].zfill(2)
        super_info += hex(len(hex(self.size)) - 2)[2:]
        self.write(super_info.encode())
