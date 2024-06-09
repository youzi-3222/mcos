"""
程序入口点。
"""

import time
from minecraft.position import Position
from minecraft.world import world
from minecraft.block.range import BlockRange
from syscore.disk import Disk


def main():
    """
    主函数。
    """
    time.sleep(5)
    world.fill(BlockRange(Position(0, 5, 0), Position(0, 5, 0).delta(72, 8, 72)), 1)

    # Disk(Position(0, 5, 0), Position(0, 5, 0).delta(128, 128, 128)).generate_shell()


if __name__ == "__main__":
    main()
