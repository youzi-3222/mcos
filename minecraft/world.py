"""
世界。
"""

import time
from mcpi.minecraft import Minecraft, CmdPlayer
from minecraft.block.range import BlockRange
from minecraft.block.split import split
from minecraft.position import Position

MAX_DIST = 64
"""
填充方块时，玩家距离方块的最大距离。
"""
FILL_DELAY = 0.3
"""
填充两个像素之间的时间差。
"""


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

    def set(self, pos: Position, block: int, data: int = 0):
        """
        填充方块。
        """
        self.game.setBlock(*pos, block, data)

    def fill(
        self,
        block_range: BlockRange,
        block: int,
        data: int = 0,
        *,
        max_split: int = 8,
        hollow: bool = False,
        delay: float = FILL_DELAY,
    ):
        """
        填充范围内方块。
        """
        if hollow:
            x1, y1, z1, x2, y2, z2 = block_range
            for face in [
                BlockRange(Position(x1, y1, z1), Position(x2, y2, z1)),
                BlockRange(Position(x1, y1, z1), Position(x1, y2, z2)),
                BlockRange(Position(x1, y1, z1), Position(x2, y1, z2)),
                BlockRange(Position(x2, y2, z2), Position(x1, y1, z2)),
                BlockRange(Position(x2, y2, z2), Position(x1, y2, z1)),
                BlockRange(Position(x2, y2, z2), Position(x2, y1, z1)),
            ]:
                self.fill(face, block, data, max_split=max_split, hollow=False)
        else:
            start_pos = self.player.getPos()
            for pixel in split(block_range, max_split):
                # print(pixel)
                if (
                    abs(self.player_pos.x - pixel.p1.x) > MAX_DIST
                    or abs(self.player_pos.z - pixel.p1.z) > MAX_DIST
                ):
                    self.player.setPos(*pixel.p1.delta(1, max_split, 1))
                    time.sleep(1)
                self.game.setBlocks(*pixel, block, data)
                time.sleep(delay)
            time.sleep(1)
            self.player.setPos(*start_pos)

    def get(self, block: Position):
        """
        获取指定方块。
        """
        return self.game.getBlock(*block)


world = World()
