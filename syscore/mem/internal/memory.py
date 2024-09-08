"""
表示内存的数据类。
"""

from syscore.mem.external.dentry import Dentry


class Memory:
    """
    内存。
    """

    dentry: dict[int, Dentry] = {}
