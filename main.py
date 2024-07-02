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
    time.sleep(5)
    world.fill(BlockRange(Position(0, 5, 0), Position(0, 5, 0).delta(180, 10, 72)), 0)

    # Disk(Position(0, 5, 0), Position(0, 5, 0).delta(128, 128, 128)).generate_shell()


if __name__ == "__main__":
    main()
