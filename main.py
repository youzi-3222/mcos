"""
程序入口点。
"""

# import sys
import math
from pathlib import Path
import time

# from minecraft.position import Position

# from minecraft.world import world
# from minecraft.block.range import BlockRange
# from syscore.mem.external.coding import bytes2bin
# from syscore.mem.external.disk import Disk
from syscore.mem.external.coding import bytes2bin
from syscore.mem.external.inode import ACCESS, Inode


def main():
    """
    主函数。
    """
    # time.sleep(3)
    i = Inode(
        b"\x17p\x00\x00\x00\x003_M\x02\x00\x00\x00\x003_M\x02\x05\x00?C:/test.txt", 15
    )
    print(i.access, i.create_time, i.modify_time, i.data, i.length, i.path)
    i.access = ACCESS.READONLY
    i.create_time = math.floor(time.time())
    i.modify_time = math.floor(time.time())
    i.data = 0x500
    i.length = 3000
    i.path = Path("C:\\test.txt")
    print(bytes2bin(i.to_bytes(15)))
    # d = Disk(Position(0, 4, 0), Position(0, 4, 0).delta(16, 16, 16))
    # d.format()
    # print(d.bitmap)


if __name__ == "__main__":
    main()
