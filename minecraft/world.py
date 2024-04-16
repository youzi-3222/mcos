"""
世界。
"""

from mcpi.minecraft import Minecraft, CmdPlayer
from minecraft.block.range import BlockRange
from minecraft.block.spilt import SpiltBlockRange
from minecraft.position import Position


class World:
    """
    Minecraft 世界。
    """

    game: Minecraft
    """Minecraft 对象。"""
    player: CmdPlayer
    """玩家。"""

    def __init__(self) -> None:
        self.game = Minecraft.create()
        self.player = self.game.player

    @property
    def _player_pos(self):
        return self.player.getTilePos()

    @property
    def player_pos(self) -> Position:
        """
        玩家坐标。
        """
        pos = self._player_pos
        return Position(pos.x, pos.y, pos.z)

    def fill(
        self, block_range: BlockRange, block_id: int, data: int = 0, max_spilt: int = 8
    ):
        """
        填充范围内方块。
        """
        blocks = SpiltBlockRange(block_range.p1, block_range.p2, max_spilt)
        for pixel in blocks:
            print(pixel.list)
            self.game.setBlocks(*pixel.list, block_id, data)


world = World()
