"""
编解码。
"""


# 这校验……说实话没啥用，汉明码是针对二进制的，我们存数据不是二进制，……算了吧
class DecodeError(Exception):
    """
    解码时错误。
    """


def _hamming_encode(data: bytes) -> bytes:
    """
    汉明编码。data 必须为 11 位。
    """
    if len(data) != 11:
        raise ValueError("Data must be 12 bits long")
    if str(data).replace("0", "").replace("1", "") != "":
        raise ValueError(f"Data must be binary, got {data}")

    # 看了一下别的代码，太复杂了，不如枚举法
    p1 = data[0] + data[1] + data[3] + data[4] + data[6] + data[8] + data[10]
    p2 = data[0] + data[2] + data[3] + data[5] + data[6] + data[9] + data[10]
    p3 = data[1] + data[2] + data[3] + data[7] + data[8] + data[9] + data[10]
    p4 = data[4:10].count(1)
    p1, p2, p3, p4 = [x % 2 for x in [p1, p2, p3, p4]]
    p0 = (p1 + p2 + p3 + p4 + data.count(1)) % 2
    return bytes([p0, p1, p2, data[0], p3, *data[1:3], p4, *data[4:10]])


def _hamming_decode(data: bytes) -> bytes:
    """
    汉明解码。data 必须为 16 位。
    """
    if len(data) != 16:
        raise ValueError("Data must be 16 bits long")
    if str(data).replace("0", "").replace("1", "") != "":
        raise ValueError(f"Data must be binary, got {data}")
    actual_data = bytes(data[3]) + data[5:7] + data[9:15]
    ep0 = data[1:].count(1)
    ep1 = data[3] + data[5] + data[7] + data[9] + data[11] + data[13] + data[15]
    ep2 = data[3] + data[6] + data[7] + data[10] + data[11] + data[14] + data[15]
    ep3 = data[5] + data[6] + data[7] + data[12] + data[13] + data[14] + data[15]
    ep4 = data[9:15].count(1)
    ep0, ep1, ep2, ep3, ep4 = [x % 2 for x in [ep0, ep1, ep2, ep3, ep4]]
    p0, p1, p2, p3, p4 = data[0], data[1], data[2], data[4], data[8]
    error = [ep0 == p0, ep1 == p1, ep2 == p2, ep3 == p3, ep4 == p4]
    if error.count(False) > 3:
        raise DecodeError("Two or more digits are incorrect")
    if error.count(False) in (
        0,  # 没问题
        1,  # 校验码炸了
    ):
        return actual_data
    incorrect_index = 0
    for i in range(1, 4):
        if not error[i]:
            incorrect_index += 2 ** (i - 1)
    return (
        data[:incorrect_index]
        + bytes(not data[incorrect_index])
        + data[incorrect_index + 1 :]
    )


def bytes2digits(data: bytes) -> list[int]:
    """
    将 bytes 转换为五位整数列表。会在最后补全。
    """
    binary_str = "".join(f"{byte:08b}" for byte in data)
    padding = 5 - len(binary_str) % 5
    binary_str += "0" * padding
    return [int(binary_str[i : i + 5], 2) for i in range(0, len(binary_str), 5)]


def bin2digits(binary: str) -> list[int]:
    """
    将二进制数转换为五位整数列表。会在最后补全。
    """
    padding = 5 - len(binary) % 5
    binary += "0" * padding
    return [int(binary[i : i + 5], 2) for i in range(0, len(binary), 5)]


def digits2bytes(decimal: list[int], padding: int = 0) -> bytes:
    """
    将五位整数列表转为 bytes。
    """
    # 拼接所有二进制字符串
    binary_str = "".join(f"{num:05b}" for num in decimal)

    # 从二进制字符串中读取字节
    bytes_list = [int(binary_str[:padding], 2)] if padding != 0 else []
    for i in range(padding, len(binary_str), 8):
        byte_str = binary_str[i : i + 8]
        if len(byte_str) < 8:
            break
        bytes_list.append(int(byte_str, 2))

    return bytes(bytes_list)


def digits2bin(decimal: list[int]) -> str:
    """
    将五位整数列表转为二进制。
    """
    # 拼接所有二进制字符串
    return "".join(f"{num:05b}" for num in decimal)


def bin2bytes(binary: str) -> bytes:
    """
    将二进制字符串转为 bytes。
    """
    byte_list = bytearray()
    for i in range(0, len(binary), 8):
        byte_list.append(int(binary[i : i + 8], 2))

    return bytes(byte_list)


def bytes2bin(data: bytes) -> str:
    """
    将 bytes 转为二进制字符串。
    """
    return "".join(f"{byte:08b}" for byte in data)
