"""
文件系统。

### 命名

- `_sys_*`：文件系统相关 IO 方法。
- `fd_*`：文件描述符相关方法。
"""

from pathlib import Path
from syscore.mem.external.disk import Disk


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

    def fd_open(self, path: Path, mode: str = "r", encoding: str = "utf-8"):
        """
        打开文件。
        """
        if path.drive not in self.disks:
            raise FileNotFoundError(f"Disk {path.drive} not found.")

    def _sys_write(self, path: Path, content: str):
        """
        写入文件。
        """
