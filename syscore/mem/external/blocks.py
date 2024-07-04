"""
数据与方块对照表。
"""

BLOCKS = [
    0,  # air
    1,  # stone
    3,  # dirt
    4,  # cobblestone
    5,  # wooden_plank      5
    14,  # gold_ore
    15,  # iron_ore
    16,  # coal_ore
    17,  # log
    20,  # glass            10
    24,  # sandstone
    25,  # noteblock
    35,  # wool
    41,  # gold_block
    42,  # iron_block       15
    45,  # brick
    47,  # bookshelf
    49,  # obsidian
    56,  # diamond_ore
    57,  # diamond_block    20
    58,  # crafting_table
    61,  # furnace
    84,  # jukebox
    85,  # fence
    86,  # pumpkin          25
    87,  # netherrock
    88,  # soul_sand
    89,  # glowstone
    95,  # stained_glass
    98,  # stonebrick       30
    101,  # iron_bars
    102,  # glass_pane
]


def _get_block(data: int) -> int:
    """
    获取方块 ID。`data` 需在 0-31 之间。
    """
    return BLOCKS[data]


def _get_data(block: int) -> int:
    """
    获取方块数据。不抛出异常。
    """
    try:
        return BLOCKS.index(block)
    except ValueError:
        return 0


def digits2block(data: list[int]) -> list[int]:
    """
    将数据编码为方块 ID。每个数据值需在 0-31 之间。
    """
    try:
        return [_get_block(x) for x in data]
    except KeyError as e:
        raise ValueError("Invalid data") from e


def block2digits(data: list[int]) -> list[int]:
    """
    将方块 ID 解码为五位数据。
    """
    return [_get_data(x) for x in data]
