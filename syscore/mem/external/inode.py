"""
索引节点。
"""

import enum
from pathlib import Path
from typing import Optional, overload

from syscore.base import int2bin
from syscore.mem.external.coding import bin2bytes, bytes2bin


class ACCESS(enum.Enum):
    """
    访问权限。
    """

    READONLY = 0
    """只读。"""
    NORMAL = 1
    """正常。任何用户都可读写。"""
    ADMIN = 2
    """管理员。只有管理员可读写，普通用户只读。"""
    SYSTEM = 3
    """系统。只有系统可读写，任何用户只读。"""


ACCESS_LENGTH = 4
"""
访问权限的长度，位。

留这个常量的原因是，我之后有极大可能会拓展上面那个枚举。
"""


class Inode:
    """
    索引节点。
    """

    loc: int
    """索引节点所在逻辑块。"""
    length: int
    """文件大小，位。"""
    access: ACCESS
    """访问权限。"""
    create_time: int
    """创建时间的时间戳。"""
    modify_time: int
    """修改时间的时间戳。"""
    data: int
    """数据指针。"""
    path: Path
    """文件的完整路径。"""

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, loc: int, inode: bytes, ptr_len: int): ...
    def __init__(
        self,
        loc: Optional[int] = None,
        inode: Optional[bytes] = None,
        ptr_len: Optional[int] = None,
    ):
        if loc is None or inode is None or ptr_len is None:
            return
        try:
            self.loc = loc
            self.path = Path(inode[:256].replace(b"\x00", b"").decode())
            data = bytes2bin(inode[256:])
            self.length = int(data[:ptr_len], 2)
            self.access = ACCESS(int(data[ptr_len : ptr_len + ACCESS_LENGTH], 2))
            self.create_time = int(
                data[ptr_len + ACCESS_LENGTH : ptr_len + 64 + ACCESS_LENGTH], 2
            )
            self.modify_time = int(
                data[ptr_len + 64 + ACCESS_LENGTH : ptr_len + 128 + ACCESS_LENGTH], 2
            )
            self.data = int(
                data[ptr_len + 128 + ACCESS_LENGTH : 2 * ptr_len + 128 + ACCESS_LENGTH],
                2,
            )
        except KeyError as e:
            raise ValueError(f"无效的 inode 数据（{ptr_len}）：{inode}。") from e

    def to_bytes(self, ptr_len: int) -> bytes:
        """
        将 inode 转换为 bytes。
        """
        result = self.path.as_posix().split(":", 1)[1][1:].encode().ljust(256, b"\x00")
        bin_result = ""
        bin_result += int2bin(self.length, ptr_len)
        bin_result += int2bin(self.access.value, ACCESS_LENGTH)
        # 防止 2038 年爆炸，这里用 64 位时间戳
        bin_result += int2bin(self.create_time, 64)
        bin_result += int2bin(self.modify_time, 64)
        bin_result += int2bin(self.data, ptr_len)
        result += bin2bytes(bin_result)
        return result
