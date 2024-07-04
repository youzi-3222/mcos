"""
程序入口点。
"""

import time
from minecraft.position import Position
from minecraft.world import world
from minecraft.block.range import BlockRange
from syscore.mem.external.disk import Disk


def main():
    """
    主函数。
    """
    # time.sleep(5)
    d = Disk(Position(0, 6, 0), Position(0, 6, 0).delta(8, 16, 8))


if __name__ == "__main__":
    main()
