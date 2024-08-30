"""
程序入口点。

警告：如果你想要学习关于文件系统或操作系统的知识，切记切记
不要看这份源码！
不要看这份源码！
不要看这份源码！
这份源码里面的文件系统是经过特殊优化，以适配 Minecraft 游戏的！
不代表真实的文件系统或操作系统处理方式！！！
"""

from pathlib import Path

from mcpi.connection import RequestError

from minecraft.position import Position
from syscore.mem.external.disk import Disk
from syscore.mem.external.io import IO


def print_help():
    """
    输出帮助。
    """
    print("由于游戏处理能力的限制，IO 的过程可能需要一段时间，请耐心等待。")
    print("命令格式：")
    print("w <路径> <内容>")
    print("    写入文件。")
    # print("")
    print("r <路径>")
    print("    读取文件。")
    # print("")
    print("f <盘符>")
    print("    格式化游戏驱动器。")
    print("g <盘符>")
    print("    为游戏驱动器生成外壳。")
    print("")


def main():
    """
    主函数。
    """
    disks = {}
    while True:
        drive = input("请输入盘符（结束输入则不输入）：")
        if drive == "":
            break
        assert drive.endswith(":"), "盘符应以冒号结尾"
        assert len(drive) == 2, "盘符长度应为 2"
        assert drive[0].isalpha(), "盘符应以字母开头"

        start = input("请输入起始位置，以英文逗号分隔，例如 0,4,0：")
        assert start.count(",") == 2, "起始位置应以英文逗号分隔，例如 0,4,0"
        start = Position(*map(int, start.split(",")))

        end = input("请输入结束位置，以英文逗号分隔，例如 16,20,16：")
        assert end.count(",") == 2, "结束位置应以英文逗号分隔，例如 16,20,16"
        end = Position(*map(int, end.split(",")))

        disks.update({drive.upper(): Disk(start, end)})
    io = IO(disks)
    while True:
        try:
            cmd = input("> ")
            command = cmd.split(" ", 2)
            match command[0]:
                case "w":
                    io.write(Path(command[1]), command[2].encode("utf-8"))
                case "r":
                    print(io.read(Path(cmd.lstrip("r "))))
                    print("")
                case "f":
                    drive = command[1]
                    assert drive.endswith(":"), "盘符应以冒号结尾"
                    assert len(drive) == 2, "盘符长度应为 2"
                    assert drive[0].isalpha(), "盘符应以字母开头"
                    print("警告：")
                    print(f"游戏驱动器 {drive} 上的所有数据都将被清除！")
                    if input("是否继续 (Y/[N])>").lower().startswith("y"):
                        print("正在格式化；这可能需要一段时间，请勿退出程序。")
                        io.fs.disks[drive.upper()].format()
                case "g":
                    drive = command[1]
                    assert drive.endswith(":"), "盘符应以冒号结尾"
                    assert len(drive) == 2, "盘符长度应为 2"
                    assert drive[0].isalpha(), "盘符应以字母开头"
                    print(f"正在为 {drive} 生成外壳；这可能需要一段时间。")
                    io.fs.disks[drive.upper()].generate_shell()
                case _:
                    print_help()
        except (KeyError, IndexError):
            print_help()
        except AssertionError:
            pass
        except RequestError:
            print("请求错误，可能因为服务器未启动，或玩家不在服务器内。")


if __name__ == "__main__":
    main()
