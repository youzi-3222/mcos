"""
程序入口点。
"""

from minecraft.block.range import BlockRange
from minecraft.world import world


def main():
    """
    主函数。
    """
    world.fill(BlockRange(world.player_pos, world.player_pos.delta(20, 8, 8)), 1)


if __name__ == "__main__":
    main()
