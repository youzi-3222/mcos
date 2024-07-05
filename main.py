"""
程序入口点。
"""

import sys
import time
from minecraft.position import Position
from minecraft.world import world
from minecraft.block.range import BlockRange
from syscore.mem.external.coding import bytes2bin
from syscore.mem.external.disk import Disk


def main():
    """
    主函数。
    """
    # time.sleep(3)
    d = Disk(Position(0, 6, 0), Position(0, 6, 0).delta(16, 64, 16))
    d.loc = 0
    d.format()
    d.loc = 0
    print(d.read(100))


if __name__ == "__main__":
    main()
