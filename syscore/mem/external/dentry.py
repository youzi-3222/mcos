"""
表示目录项的数据类。
"""

from typing import Union


class Dentry:
    """
    目录项。
    """

    loc: int
    """位置。"""
    parent: int
    """父目录指针。"""
    children: list[int]
    """子文件指针列表。"""
    inode: int
    """索引节点指针。"""
    name: str
    """目录名。"""
    data: str
    """其它数据。"""

    def load(self, data: Union[bytes, dict], ptr_len: int):
        """
        从 bytes 或 dict 中加载数据。
        """
        try:
            if isinstance(data, dict):
                self.loc = data["loc"]
                self.parent = data["parent"]
                self.children = data["children"]
                self.inode = data["inode"]
                self.name = data["name"]
            elif isinstance(data, bytes):
                data_list = data.split(b",")

                self.parent = int(data[:ptr_len], 16)
                self.inode = int(data[ptr_len : 2 * ptr_len], 16)

                children = data_list[0][2 * ptr_len :]
                self.children = []
                for i in range(len(children) // ptr_len):
                    self.children.append(
                        int(children[i * ptr_len : (i + 1) * ptr_len], 16)
                    )

                self.name = data_list[1].decode()
                self.data = data_list[2].decode()
            else:
                raise TypeError(f"Invalid type of data: {type(data)}")
        except KeyError as e:
            raise ValueError("Invalid data") from e

    def tobytes(self, ptr_len: int):
        """
        将目录项转为硬盘可以存储的 bytes。
        """
        result = bytearray()
        result.extend(hex(self.parent)[2:].zfill(ptr_len).encode())
        result.extend(hex(self.inode)[2:].zfill(ptr_len).encode())
        for child in self.children:
            result.extend(hex(child)[2:].zfill(ptr_len).encode())
        result.extend(b",")
        result.extend(self.name.encode())
        result.extend(b",")
        result.extend(self.data.encode())
        return bytes(result)

    def todict(self):
        """
        转为可缓存的 dict 对象。
        """
        return {
            "loc": self.loc,
            "parent": self.parent,
            "children": self.children,
            "inode": self.inode,
            "name": self.name,
        }
