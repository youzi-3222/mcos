"""
硬盘。
"""

import math
from minecraft.block.range import BlockRange
from minecraft.position import Position
from minecraft.world import world
from syscore.mem.external.blocks import digits2block, block2digits, get_block, get_data
from syscore.mem.external.coding import (
    bin2digits,
    bytes2digits,
    digits2bytes,
    bin2bytes,
    bytes2bin,
)

VERSION_CODE = 1
"""
版本号。
"""
INODE_RATE = 0.05
"""
索引节点占硬盘总空间的比例。
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
        """磁头指针指向的方块。"""
        block = self.loc // 5
        return self.p1.delta(
            (block // self.delta_y) % self.delta_x,
            block % self.delta_y,
            block // (self.delta_x * self.delta_y),
        )

    @property
    def loc_bin(self):
        """磁头指针指向方块的二进制数据。"""
        return bin(get_data(world.get(self.loc_pos))).replace("0b", "").zfill(5)

    @loc_bin.setter
    def loc_bin(self, other: str):
        world.set(self.loc_pos, get_block(world.get(self.loc_pos)), int(other, 2))

    @property
    def loc_int(self):
        """磁头指针指向方块的整数数据。可能不完整。"""
        return get_data(world.get(self.loc_pos))

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

    ptr_len: int
    """指针长度。"""

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
        # 说白了，就是从一堆方块里面整出二进制数据，然后拿出我想要的
        padding = self.loc % 5
        start_pos = self.loc
        binary = ""
        for _ in range(length // 5 + 2):
            binary += self.loc_bin
            self.loc += 5

        self.loc = start_pos + length
        return bin2bytes(binary[padding : padding + length])

    def write(self, data: bytes):
        """
        写入。
        """
        # 其实就是把二进制数据补全，然后写进方块
        padding = self.loc % 5
        binary = self.loc_bin[:padding]
        print(binary)
        if padding != 0:
            self.loc -= padding
        binary += bytes2bin(data)
        print(binary)
        blocks = digits2block(bin2digits(binary))
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 5
        self.loc -= 5 - len(binary) % 5

    def _clear(self):
        """
        清空。
        """
        try:
            self.loc = 0
            while True:
                self.write(b"\x00\x00\x00\x00\x00")
        except ValueError:
            self.loc = 0
            return True
        except:  # pylint: disable=W0702
            self.loc = 0
            return False

    def format(self, logical: int = 1024):
        """
        格式化（未测试）。

        ### 参数
        - `logical`：每个逻辑块的大小，单位为五位二进制（个方块）。
        """
        # self._clear()
        self.loc = 0

        self.write(hex(VERSION_CODE)[2:].zfill(2).encode())  # 版本号
        self.write(hex(len(hex(self.size)) - 2)[2:].zfill(1).encode())  # 指针长度
        self.ptr_len = len(hex(self.size)) - 2
        # 计算逻辑块长度
        logical_count = math.floor(self.size / logical)
        self.write(
            hex(logical_count + 3 + self.ptr_len)[2:].zfill(self.ptr_len).encode()
        )  # 索引节点指针

        self.write((logical_count * "0").encode())  # 位图
