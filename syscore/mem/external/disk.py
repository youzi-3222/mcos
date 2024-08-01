"""
硬盘。
"""

import math
from typing import Optional
from minecraft.block.range import BlockRange
from minecraft.position import Position
from minecraft.world import world
from syscore.mem.external.blocks import digits2block, get_block, get_data
from syscore.mem.external.coding import bin2digits, bin2bytes, bytes2bin
from syscore.base import int2bin

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
        """磁头指针位置（位）。"""
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
        """磁头指针指向方块的二进制数据。总是五位。"""
        return bin(get_data(world.get(self.loc_pos))).replace("0b", "").zfill(5)

    @loc_bin.setter
    def loc_bin(self, other: str):
        world.set(self.loc_pos, get_block(int(other, 2)))

    @property
    def loc_int(self):
        """磁头指针指向方块的整数数据。总是五位二进制。"""
        return get_data(world.get(self.loc_pos))

    @property
    def bit(self) -> int:
        """大小，单位为字节（8 位）。"""
        return math.floor(self.size * 0.625)

    @property
    def size(self) -> int:
        """大小，单位为五位二进制。"""
        return round(self.delta_x) * round(self.delta_y) * round(self.delta_z)

    ptr_len: int
    """指针长度（位）。"""
    logical_len: int
    """逻辑块长度（位）。"""

    @property
    def actual_logical(self) -> int:
        """实际逻辑块长度（位）。"""
        return self.logical_len - self.ptr_len - 1

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

    def _load_super(self):
        """
        加载超级块。未完成。
        """
        self.loc = 0
        int(self.read(2 * 8).decode(), 16)

    def _read_num(self, length_bin: int) -> int:
        """
        读取数字。
        """
        padding = self.loc % 5
        start_pos = self.loc
        binary = ""
        for _ in range(length_bin // 5 + 2):
            binary += self.loc_bin
            self.loc += 5

        self.loc = start_pos + length_bin
        return int(binary[padding : padding + length_bin], 2)

    def read(self, length_bin: int) -> bytes:
        """
        读取。
        """
        # 说白了，就是从一堆方块里面整出二进制数据，然后拿出我想要的
        padding = self.loc % 5
        start_pos = self.loc
        binary = ""
        for _ in range(length_bin // 5 + 2):
            binary += self.loc_bin
            self.loc += 5

        self.loc = start_pos + length_bin
        return bin2bytes(binary[padding : padding + length_bin])

    def _write_bin(self, data: str):
        """
        写入二进制数据。
        """
        if data.startswith("0b"):
            data = data[2:]
        padding = self.loc % 5
        binary = self.loc_bin[:padding]
        if padding != 0:
            self.loc -= padding
        binary += data
        blocks = digits2block(bin2digits(binary))
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 5
        self.loc -= 5 - len(binary) % 5

    def _write_num(self, data: int, length_hex: int):
        """
        写入数字。
        """
        # 其实就是把二进制数据补全，然后写进方块
        padding = self.loc % 5
        binary = self.loc_bin[:padding]

        if padding != 0:
            self.loc -= padding
        binary += int2bin(data, length_hex * 4)

        blocks = digits2block(bin2digits(binary))
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 5
        self.loc -= 5 - len(binary) % 5

    def write(self, data: bytes):
        """
        写入。
        """
        # 其实就是把二进制数据补全，然后写进方块
        padding = self.loc % 5
        binary = self.loc_bin[:padding]

        if padding != 0:
            self.loc -= padding
        binary += bytes2bin(data)

        blocks = digits2block(bin2digits(binary))
        for block in blocks:
            world.set(self.loc_pos, block)
            self.loc += 5
        self.loc -= 5 - len(binary) % 5

    def logical_write(
        self, logical: int, data: bytes, is_dentry: Optional[bool] = None
    ):
        """
        写入逻辑块（未完成）。
        """
        raise NotImplementedError("未完成：写入逻辑块")
        self.loc = logical * self.logical_len
        if is_dentry is not None:
            self._write_bin("1" if is_dentry else "0")  # 指明是否为目录项
        else:
            self.loc += 1  # 不操作
        for i in range(len(data) // self.actual_logical):
            self.write(data[i * self.actual_logical : (i + 1) * self.actual_logical])
        self.write(data[(len(data) // self.actual_logical) * self.actual_logical :])

    def logical_clear(self, logical: int):
        """
        清空逻辑块。
        """
        self.loc = logical * self.logical_len
        self._write_bin("0" * self.logical_len)

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
        格式化。

        ### 参数
        - `logical`：每个逻辑块的大小，单位为字节。
        """
        if not 512 <= logical <= 0xFFFF:
            raise ValueError(f"逻辑块大小不合法：应为 [512, 65535]，实为 {logical}。")
        self._clear()
        self.loc = 0
        self.logical_len = logical * 8

        self._write_bin("0")  # 超级块也要指明是否为目录项
        self._write_num(VERSION_CODE, 2)  # 版本号
        self._write_num(logical, 4)  # 逻辑块长度
        self.ptr_len = len(bin(self.size)) - 2
        self._write_num(self.ptr_len, 1)  # 指针长度
        # 计算逻辑块长度
        logical_count = math.floor(self.bit / logical)

        self._write_bin((logical_count * "0"))  # 位图
