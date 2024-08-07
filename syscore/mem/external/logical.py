"""
表示逻辑块的数据类。
"""

from dataclasses import dataclass


@dataclass
class Logical:
    """
    逻辑块。
    """

    is_dentry: bool
    """是否为目录项。"""
    data: bytes
    """数据。"""
    next_logical: int
    """下一个逻辑块的序号。"""
