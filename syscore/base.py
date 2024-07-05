"""
基础方法。
"""

from typing import Optional


def int2hex(num: int, length: Optional[int] = None) -> str:
    """
    转为 16 进制字符串。

    - `num`: `12_648_430`
    - `length`: `8`
    - `return`: `00c0ffee`
    """
    return hex(num)[2:].zfill(length) if length else hex(num)[2:]


def int2bin(num: int, length: Optional[int] = None) -> str:
    """
    转为 2 进制字符串。

    - `num`: `12_648_430`
    - `length`: `32`
    - `return`: `00000000110000001111111111101110`
    """
    return bin(num)[2:].zfill(length) if length else bin(num)[2:]
