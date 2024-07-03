"""
编解码。
"""


def bytes2digits(data: bytes) -> list[int]:
    """
    将 bytes 转换为五位整数列表。
    """
    binary_str = "".join(f"{byte:08b}" for byte in data)
    # print(binary_str)

    padding = 5 - len(binary_str) % 5
    binary_str += "0" * padding
    # print(binary_str)

    return [int(binary_str[i : i + 5], 2) for i in range(0, len(binary_str), 5)]


def digits2bytes(decimal: list[int]) -> bytes:
    """
    将五位整数列表转为 bytes。
    """
    # 拼接所有二进制字符串
    binary_str = "".join(f"{num:05b}" for num in decimal)

    # 从二进制字符串中读取字节
    # 注意：这里我们假设 binary_str 的长度是 8 的倍数，或者我们至少可以处理到它结束的地方
    bytes_list = []
    for i in range(0, len(binary_str), 8):
        byte_str = binary_str[i : i + 8]
        if len(byte_str) < 8:
            # 预期最后补的是零
            if "1" in byte_str:
                raise ValueError("Invalid binary string")
            break
        bytes_list.append(int(byte_str, 2))

    return bytes(bytes_list)
