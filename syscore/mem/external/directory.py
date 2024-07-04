"""
表示目录的数据类。
"""

from typing import Optional


class Dentry:
    """
    目录项。
    """

    loc: int
    """位置。"""
    parent: int
    """父目录指针。"""
    child_dir: list[int]
    """子目录指针列表。"""
    child_files: list[int]
    """文件指针列表。"""
    inode: int
    """索引节点指针。"""
    name: str
    """目录名。"""

    def __init__(self, loc: Optional[int]):
        if loc:
            self.loc = loc

    def tobytes(self, ptr_len: int):
        """
        将目录项转为硬盘可以存储的文件。
        """
        result = bytearray()
        result.extend(hex(self.parent)[2:].zfill(ptr_len).encode())
        result.extend(hex(self.inode)[2:].zfill(ptr_len).encode())
        for child in self.child_dir:
            result.extend(hex(child)[2:].zfill(ptr_len).encode())
        result.extend(b",")
        for file in self.child_files:
            result.extend(hex(file)[2:].zfill(ptr_len).encode())
        result.extend(b",")
        result.extend(self.name.encode())
        return bytes(result)

    def todict(self):
        """
        转为可缓存的 dict 对象。
        """
        return {
            "loc": self.loc,
            "parent": self.parent,
            "child_dir": self.child_dir,
            "child_files": self.child_files,
            "inode": self.inode,
            "name": self.name,
        }
