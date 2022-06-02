# Hadoop生态系统

> **Hadoop**是一个开源的、可运行大规模集群上的分布式计算平台
>
> **基于Java**语言开发的，具有很好的跨平台特性，可以部署在廉价的计算机集群中。
>
> 核心是**Hadoop分布式文件系统（HDFS*）和MapReduce***
>
> 借助于Hadoop，程序员可以轻松地编写分布式并行程序，并将其运行于计算机集群上，完成海量数据的存储与分析处理。

## 12.1 Hadoop总体架构

### **系统架构：**

- 部署在低成本的Intel/Linux硬件平台上

- 由多台装有Intel x86处理器的服务器或PC机组成

- 通过高速局域网构成一个计算集群

- 各个节点上运行Linux操作系统

### **三大主要模式：**

- 单机模式（standalone mode）

- 虚拟分布模式（pseudo-distributed mode）

- 完全分布模式（completely distributed Mode）

### **集群配置**：

- 硬件配置：

NameNode（**执行作业调度、资源调配、系统监控等任务**）

DataNode（**承担具体的数据计算任务**）

- 软件配置：

Linux O/S

JDK 1.6以上版本

SSH（Security Shell）安全协议

- 网络配置：

NameNode到机架（Rack）的网络连接

机架内部的DataNode之间的网络连接

#### 集群软件配置：

- 主节点运行的程序或进程：

  - 主节点程序Namenode

  - Jobtracker 守护进程

  - 管理集群所用的Hadoop 工具程序和集群监控浏览器

- 从节点运行的程序：

  - 从节点程序Datanode

  - 任务管理进程Tasktracker

- 区别：主从结点的分工

**主节点程序提供 Hadoop 集群管理、协调和资源调度功能**

**从节点程序主要实现 Hadoop 文件系统（HDFS）存储功能和节点数据处理功能。**

#### **Hadoop软件架构：**

- 组成：

  - 基于**HDFS/HBase**的数据存储系统

  - 基于**YARN/Zookeeper**的管理调度系统

  -  支持不同计算模式的处理引擎

##### 数据存储系统

- 组成：

  - 分布式文件系统**HDFS（Hadoop Distributed File System）**

  - 分布式非关系型数据库Hbase

  - 数据仓库及数据分析工具Hive和Pig

  - 用于数据采集、转移和汇总的工具Sqoop和Flume。

- HDFS文件系统构成了Hadoop数据存储体系的**基础**

##### 管理调度系统

- **Zookeeper：提供分布式协调服务管理**

- **Oozie：负责作业调度**

- Ambari：提供集群配置、管理和监控功能

- Chukwa：大型集群监控系统

- **YARN：集群资源调度管理系统**

### 总体架构图

<img src="/Users/bytedance/uestc/big_data/note/pic/pic12.png" alt="pic12" style="zoom:100%;" />

## 12.2 HDFS文件系统

### 分布式文件系统

- 结构：

  - **物理存储资源**和**对象**分散存储在通过网络相连的**远程节点**上

  - **主控服务器**（也称元数据服务器）：**负责管理命名空间和文件目录**

  - **远程数据服务器**（也称存储服务器）节点：**存储实际文件数据**

- 特点

  - 透明性
  - 高可用性
  - 支持并发访问
  - 可扩展性
  - 安全性

<img src="/Users/bytedance/uestc/big_data/note/pic/pic13.png" alt="pic12" style="zoom:100%;" />

**唯一的主节点**：运行NameNode，JobTreacker，Zookeeper、Hmaster等负责集群管理、资源配置、作业调度的程序

**多个从结点：承担数据存储和计算任务**

**客户端：用于支持客户操作HDFS**

#### HDFS架构

- Master/Slave架构，集群中只设置一个主节点
- 优点：
  - 简化了系统设计
  - 元数据管理和资源调配更容易
- 缺
  - **命名空间的限制**：由于管理命名空间的名称节点进程是保存在内存中，因此名称节点能够容纳的对象（文件、块）的个数会受到内存空间大小的限制。
  - **性能的瓶颈**：整个分布式文件系统的吞吐量，受限于单个名称节点的吞吐量
  - **单点失效（SPOF）问题**：一旦这个唯一的名称节点发生故障，会导致整个集群变得不可用

### 12.2.2 HDFS存储结构

- 以**块为基本单位存储文件**
- 文件被划分为**64MB大小的多个blocks**，属于**同一个文件的blocks**分散存储在**不同的DataNode**上面
- 处于系统容错需要，每一个block有多个**副本（replica）**，存储在不同的DataNode上面
- 每个DataNode上的数据存储在本地的Linux文件系统上

<img src="/Users/bytedance/uestc/big_data/note/pic/pic14.png" alt="pic12" style="zoom:50%;" />

#### HDFS存储结构优势：

- **有利于大规模文件存储**：一个大规模文件可以被分拆成若干个文件块，不同的文件块可以被分发到不同的节点上，因此，一个文件的大小不会受到单个节点存储容量的限制。

- **适合数据备份**：每个文件块都可以冗余存储到多个节点上，大大提高了系统的容错性和可用性。

- **系统设计简化**：首先简化了存储管理，因为文件块大小是固定的，这样就可以很容易计算出一个节点可以存储多少文件块；其次方便了元数据的管理，元数据不需要和文件块一起存储，可以由其他系统负责管理元数据。

要实现上述基于块的存储机制，HDFS需解决三个问题：**文件-块-节点的映射关系，命名空间管理，文件读写操作流程。**

### 1. HDFS命名空间管理

- 命名空间包括**目录、文件和块**

- 文件 -> block -> 节点的映射关系作为元数据存储在**Namenode上**

- 整个HDFS集群只有**一个命名空间**，由**唯一的一个名称节点负责对命名空间进行管理**

- HDFS使用的**是传统的分级文件体系**

- NameNode进程使用**FsImage**和**EditLog**对命名空间进行管理

  - **FsImage：**
    - 存储和管理内容：
      - 文件系统目录树
      - 目录树中所有文件和文件夹的元数据，inode
    - 由名称节点进程把文件 -> block -> 节点映射关系表装载并保留在内存中

  - **EditLog：**
    - 是NameNode启动后对文件系统改动操作的记录

<img src="/Users/bytedance/uestc/big_data/note/pic/pic15.png" alt="pic12" style="zoom:100%;" />

<img src="/Users/bytedance/uestc/big_data/note/pic/pic16.png" alt="pic12" style="zoom:50%;" />

### 2. 第二名称节点

- 作用

  - 保存名称节点NameNode对HDFS元数据信息的备份
  - 减少名称节点NameNode重启的时间

- 一般独立部署在一台机器上

- 工作流程：

  - Roll edits：SecondaryNameNode进程会定期和NameNode通信，请求其停止使用 EditLog文件，暂时将新的写操作写到一个新的文件edit.new上来，这个操作是瞬间完成的，上层写日志的函数完全感觉不到差别。

  - Retrieve FsImage and edits from NameNode：Secondary NameNode进程通过HTTP GET方式从NameNode取得FsImage和EditLog文件，并下载到本地相应目录下。

  - Merge：SecondaryNameNode进程将下载的FsImage载入到内存，然后一条一条地执行EditLog文件中的各项更新操作，使得内存中的FsImage保持最新，这个过程就是EditLog和FsImage文件的合并。

  - Transfer checkpoint to NameNode：Secondary NameNode执行完操作（3）之后，会通过post方式将新的FsImage文件发送到NameNode节点上。

  - Roll again: NameNode将从SecondaryNameNode接收到的新的FsImage替换旧的FsImage文件，同时将edit.new替换为原来的EditLog文件，此过程使得EditLog文件重新变小

### 3. HDFS文件读写机制

- 主要访问方式：

  - HDFS shell命令

  - HDFS Java API 

- **HDFS读文件流程（以JAVA为例）**

  ![pic18](/Users/bytedance/uestc/big_data/note/pic/pic18.png)

- **HDFS写文件流程**

<img src="/Users/bytedance/uestc/big_data/note/pic/pic17.png" alt="pic17" style="zoom:50%;" />

### 4. HDFS数据容错与恢复

HDFS在硬件故障情况下保障**可用性和可靠性**，通过数据**冗余备份、副本存放策略、容错与恢复机制来提供这种高可用性**。

#### 1、多副本方式进行冗余存储

- 加快数据传输速度

- 容易检查数据错误

- 保证数据可用性

#### 2、机架感知副本存放策略

改进数据的可靠性、可用性和网络宽带的利用率

防止某一机架失效时数据丢失

利用机架内的高带宽特性提高数据读取速度

- 存放流程

  - block1放到与客户端同一机架的一个节点

  - block2放到block1所在机架之外的节点

  - block3放在与block2同一机架的另一节点

    <img src="/Users/bytedance/uestc/big_data/note/pic/pic19.png" alt="pic19" style="zoom:75%;" />

    <img src="/Users/bytedance/uestc/big_data/note/pic/pic20.png" alt="pic19" style="zoom:75%;" />

  - 存放流程

    - HDFS提供了一个API可以确定某一数据节点所属的机架ID
    - 客户端从名称节点获得不同副本的存放位置列表
    - 调用API确定这些数据节点所属的机架ID
    - 发现ID匹配：优先读取该数据节点存放的副本
    - 没有发现：随机选择一个副本读取数据

  - 

#### 3、错误检测和恢复机制

包括NameNode检测、DataNode检测和数据错误检测

- NameNode检测：第二名称节点

- DataNode检测：心跳检测，DataNode周期性的向集群NameNode发送心跳包和块报告

- 数据错误检测：CRC循环校验

| **出现情况**                                       | **应对**                                                   |
| -------------------------------------------------- | ---------------------------------------------------------- |
| 规定时间内未收到心跳报告                           | 将该DataNode标记为失效                                     |
| 数据块副本的数目低于设定值                         | 启动数据冗余复制，为该数据块生成新的副本，放置在另外节点上 |
| 数据副本损坏、DataNode上的磁盘错误或者复制因子增大 | 触发复制副本进程                                           |

## 12.3 资源管理和作业调度

- 多节点、多任务、并行计算的分布式系统，工作需要解决的问题
  - 不同节点、不同计算任务之间的协同管理
  - 分布式作业的调度和执行机制
  - 分布式系统中的资源和数据共享协调方法
- 实现的三大组件
  - Zookeeper提供分布式协同服务
  - Oozie 提供作业调度和工作流执行
  - YARN 提供集群资源管理服务

### 12.3.1 Zookeeper

- 我们为什么需要Zookeeper？

我们需要一个用起来像单机但是又比单机更可靠的东西。

- Zookeeper采用主-从架构
  - ZooKeeper服务由一组2n+1台的Server节点组成