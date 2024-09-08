"""
文件系统。

### 命名

- `sys_*`：文件系统相关 IO 方法。
- `fd_*`：文件描述符相关方法。
"""

import math
from pathlib import Path
import time
from syscore.mem.external.disk import Disk
from syscore.mem.external.fd import Fd
from syscore.mem.external.inode import ACCESS, Inode


class FileSystem:
    """
    文件系统。
    """

    disks: dict[str, Disk] = {}
    """
    硬盘。
    
    - Key：盘符，例如 `C:` `D:`。
    - Value：硬盘对象。
    """
    fd_list: dict[int, Fd] = {}

    def __init__(self, disks: dict[str, Disk]):
        self.disks = disks.copy()
        for k, d in self.disks.items():
            try:
                d.load()
            except:
                match input(
                    f"硬盘 {k} 存在问题或未初始化，需要格式化。如果不格式化，则它将不可用。是否现在格式化 (Y/[N])?"
                ).lower():
                    case "y":
                        d.format()
                    case _:
                        del disks[k]
        self.disks = disks

    def fd_open(self, path: Path, mode: str = "r"):
        """
        打开文件。
        """
        assert (drive := path.drive) in self.disks, f"Disk {drive} not found."
        inode = self.disks[drive].searchfor(path)
        # print(inode.access, inode.create_time, inode.data, inode.loc)
        if not inode:
            inode = Inode()
            inode.access = ACCESS.NORMAL
            inode.create_time = math.floor(time.time())
            inode.data = 0
            inode.length = 0
            inode.modify_time = math.floor(time.time())
            inode.path = path
            (d := self.disks[drive]).logical_write(
                (inode_loc := d.get_valid_logical()), inode.to_bytes(d.ptr_len), True
            )
            inode.loc = inode_loc
        if inode.loc in self.fd_list:
            if (
                "w" not in (fd := self.fd_list[inode.loc]).mode + mode
                and "a" not in fd.mode + mode
            ) or fd.is_closed:
                self.fd_list[inode.loc].open_count += 1
                return fd
            raise FileExistsError(f"File {path} is already opened.")
        self.fd_list.update({inode.loc: (fd := Fd(drive, inode, mode))})
        return fd

    def sys_write(self, fd: Fd, content: bytes):
        """
        写入文件。
        """
        d = self.disks[fd.drive]
        if fd.inode.data == 0:
            fd.inode.data = d.get_valid_logical() * d.logical_len
            d.logical_write(fd.inode.loc, fd.inode.to_bytes(d.ptr_len))
        d.logical_write(fd.inode.data // d.logical_len, content)

    def sys_read(self, fd: Fd):
        """
        读取文件。
        """
        d = self.disks[fd.drive]
        return d.logical_read(fd.inode.data // d.logical_len).data
