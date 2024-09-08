"""
应用层 IO 接口。
"""

from pathlib import Path

from syscore.mem.external.filesystem import FileSystem, Disk


class IO:
    """
    IO 接口。
    """

    def __init__(self, disks: dict[str, Disk]):
        self.fs = FileSystem(disks)

    def write(self, path: Path, content: bytes):
        """
        写入文件。
        """
        fd = self.fs.fd_open(path, "w")
        self.fs.sys_write(fd, content)

    def read(self, path: Path):
        """
        读取文件。
        """
        fd = self.fs.fd_open(path, "r")
        result = self.fs.sys_read(fd).replace(b"\x00", b"")
        fd.close()
        return result
