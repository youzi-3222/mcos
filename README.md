# MinecraftOS

## 致歉

由于计划有变，自 2024 年 12 月 29 日起，该项目标为 Archive，我不再继续维护该项目，很抱歉。

您可以通过邮箱联系我：`youzi5201086@163.com`。以下内容仅供存档。

## 概述

这是一个在 Minecraft 中制作的简单操作系统，主要用于整活。嗯。

本人初三（2024 年读初三），开学之后可能没空处理反馈，如果急的话可以直接写了交 PR……

PS：别骂了别骂了，是我菜，只会写 Python……

## 运行

1. 启动 Minecraft 1.12 服务器。需安装 [RaspberryJuice](https://github.com/zhuowei/RaspberryJuice) 插件。
2. 启动 `main.py`。

```bash
python main.py
```

## 贡献

在此表示道歉，由于计划调整，我不再对该项目进行维护，不接受 Issue 或 Pull Request。

您可以克隆该储存库，并按照 LICENSE 文件中的规定使用源代码。

下面还有一些文档，希望能帮助您看懂我的代码（💩）。

## 定义 / 消歧义

- **位**：一个二进制码所占空间为一位。
- **字节**：八位组成的数据所占空间为一字节。
- **五位**（五位二进制）：五位组成的数据所占空间，或游戏中一格方块最多能存储的数据为五位。
- **硬盘**：游戏中手动划出的一块三维的区域为硬盘。
- **块**：硬盘格式化时，划分的若干个相同长度的区域为块。
- **指针**：表示硬盘上任意一位位置的一串数据为指针。
- **指针长度**：一个硬盘最多可存储的位数所占的位数，或指向硬盘任意位置的指针所占位数为指针长度，并且是硬盘的固定属性。

## 文件系统

在我这里，文件系统设计的准绳就是：**求同存异**。

- 求同，即大部分设计都使用当前常用的文件管理方式。
- 存异，即根据实验结果、游戏本身特性、效率等等方面，对文件管理进行一些优化。

你可能现在还没看懂是什么意思。到了下面，你就能看懂了。

### 基础

使用方块的组合（见 [syscore/mem/external/blocks.py](./syscore/mem/external/blocks.py)）存储数据，每个方块可以存储五位二进制。

但是我最担心的事情还是发生了。

字节（八个二进制）和方块（五个二进制）完全不兼容，他俩完全就是互素的。

这就直接导致 write 一次和分开来 write 两次不幂等。

这不仅带来了资源的浪费，还直接导致：同时读取这两段*分开来写的*数据时，会出现乱码。

怎么解决？

1. 尽量只写一次就达到最终效果。写入文件的时候，给个缓存让用户操作，关闭文件之后再给存进去。
2. 把指针精确到二进制。

思来想去还是选择方案二更好，更符合用户直观感受。

### 硬盘

每个硬盘开头的第一个逻辑块有一串数据，指示其信息。其格式如下：

| 长度 | 含义               | 示例 |
| ---- | ------------------ | ---- |
| 2    | 版本号             | 2c   |
| 4    | 逻辑块长度（字节） | 0400 |
| 3    | 指针长度 $n$       | 6    |

~~看我多聪明，还留了两位版本号~~

目前硬盘版本号为 `0`。请理解，**目前该项目处于测试状态，不保证向上兼容性**，请在使用时考虑这一点。

紧随其后的是位图，指示每个逻辑块的使用情况。如果硬盘总空间为 $s$ 字节，逻辑块长度为 $b$ 字节，那么位图长度 $c$ 位为：

$$
c=\lfloor \frac{s}{b} \rfloor.
$$

格式化硬盘时，分配逻辑块。每个逻辑块开头一位指示其存储的是否是索引节点（inode）：`1` 为 inode，`0` 为实际数据，超级块或未分配。最后 $n$ 位指示下一个逻辑块的指针。

有一点非常例外：假设一个 inode 非常非常长，占用了 2 个甚至多个逻辑块，那么只有第一个逻辑块标记为 inode，其余均不标记。这是为了防止错误地从中间开始读取 inode。

*特别注意：指向逻辑块的指针应指向逻辑块第一位。*

由于服务端处理能力有限，读取速度稳定在约 `100` 字节每秒，请在使用时考虑到这一点，并尽可能减少 IO 次数。

### 索引节点（inode）

索引节点是文件的 **唯一** 标识。

索引节点格式如下（`ptr` 为指针长度）：

| 长度     | 描述     | 举例                              |
| -------- | -------- | --------------------------------- |
| 256 字节 | 文件路径 | `b"path\\example.txt\x00\x00..."` |
| ptr      | 文件大小 | `300`                             |
| 4 位     | 访问权限 | `0`                               |
| 64 位    | 创建时间 | `GMT+08:00 2024-08-23 12:43:18`   |
| 64 位    | 修改时间 | `GMT+08:00 2024-08-23 12:43:18`   |
| ptr      | 数据指针 | `1800`                            |

现实中，索引节点是在文件被访问时才挂载，并且文件夹也占索引节点和数据块，以此方便检索。

但是我们 **能存储的文件实在是太少了**，检索甚至拿着个完整路径全部遍历都不是不行，用两块去存一个文件夹实在是浪费。
