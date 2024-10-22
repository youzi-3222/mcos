"""
文件描述符。
"""

# class IOMODE(enum.Enum):
#     """
#     文件读写模式。
#     """

#     READ = 0
#     """只读。"""
#     WRITE = 1
#     """只写，覆盖。"""
#     READWRITE = 2
#     """同时读写。"""
#     APPEND = 3
#     """追加，不存在将会抛出错误。"""
#     CREATE = 4
#     """创建，已存在将会抛出错误。"""


# class CONTENTMODE(enum.Enum):
#     """
#     读写文件内容的模式。
#     """

#     BINARY = 0
#     """二进制模式。"""
#     TEXT = 1
#     """文本模式。"""


from syscore.mem.external.inode import Inode


class Fd:
    """
    文件描述符。
    """

    drive: str
    """盘符，例如 `C:`。"""
    inode: Inode
    """索引节点。"""
    mode: str
    """文件模式。"""
    open_count: int
    """打开计数。"""

    def __init__(self, drive: str, inode: Inode, mode: str = "r"):
        self.drive = drive
        self.inode = inode
        self.mode = mode.lower()
        self.open_count = 1

    def close(self):
        """
        关闭该文件。
        """
        self.open_count -= 1

    @property
    def is_closed(self):
        """该文件是否已经被所有进程关闭（是否可以重用该打开文件表条目）。"""
        return self.open_count == 0
