"""
世界。
"""

from mcpi.minecraft import Minecraft, CmdPlayer
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

    def _player_pos(self):
        return self.player.getTilePos()

    @property
    def player_pos(self) -> Position:
        """
        玩家坐标。
        """
        pos = self.player.getTilePos()
        return Position(pos.x, pos.y, pos.z)

    def fill(self, pos: SpiltBlockRange, block_id: int, data: int = 0):
        """
        填充范围内方块。
        """
        for p in pos:
            self.game.setBlocks(*p.list, block_id, data)
