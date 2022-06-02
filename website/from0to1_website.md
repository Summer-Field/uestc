# 从零搭建属于自己的网站

> 在字节跳动实习期间，机缘巧合认识张盛宇。看他在飞书上的个性签名留的是自己的个人网站，出于好奇便点进去逛了逛。逛了一会儿后便发现，这就是我想要的可以记录自己的生活、学习的绝佳工具啊！所以从此便萌生了想要自己搭建一个属于自己网站的想法。

## 前期准备工作

搭建一个网站往往需要准备以下几个材料：

- 属于自己的云服务器  --  compulsory

购买云服务器大多都十分昂贵，但是不少大厂的云厂商都提供了校园优惠。我是在 [腾讯云 云+校园](https://cloud.tencent.com/act/campus) 上购买的”轻量应用服务器2核2G“服务器。三年仅仅需要190rmb真的超级划算。

- 属于自己的域名  --  optional

当然你可以直接使用你服务器的公网ip来访问你的网站。但是我总觉得那不够酷，也不便于我自己记忆。所以我也是在[腾讯云](https://cloud.tencent.com/act/domainsales)上购买的。选择的域名就是`summer-field.xyz`。至于为什么后缀要选择xyz：第一是我名字的首拼是xy，第二就是腾讯云给的定义`xyz = "幸运者"` ，还蛮酷的哈lol

## 正式开始搭建自己的website

在网上看了好多资料，总结一下一共有几种方法来搭建网站

- 自己手动构建[LAMP(Linux, Apache/Nginx, MySQL, PHP)](https://en.wikipedia.org/wiki/LAMP_(software_bundle))软件栈
- [使用宝塔面板添加WordPress站点](http://tencent.yundashi168.com/558.html)
- [使用docker在SentOS上部署自己的WordPress站点](https://cloud.tencent.com/developer/article/1835064)

本着Learning By Doing的态度，我准备同时了解一下第一个和第三个方法来部署自己的的站点，可以熟悉一下linux以及docker的命令。所以这里我没有选择使用宝塔面板来搭建WordPress站点。

### Web Server选Apache还是NGINX？

> [Apache Vs NGINX – Which Is The Best Web Server for You?](https://serverguy.com/comparison/apache-vs-nginx/)

在OS、DB、Language不变的情况下，我们可以选择两种不同的Web Server，两者有什么区别？这是我值得了解和学习的。

- Apache  --  process-driven  --   create thread for each request
- NGINX  --  evnet-driven  --  handle multiple thread in one thread

这里我应该会选择NGINX来作为我的WebServer因为他更轻量，更快。我希望我的网站可以很快的访问，不希望他太复杂了。

# 问题

## 1. 使用yum安装docker出错

> DNF now has replaced YUM...

### Description

当我使用`yum update -y`升级yum后，准备使用`yum instal docker -y`在服务器上安装docker爆出如下错误

```shell
# yum install docker -y
Invalid configuration value: failovermethod=priority in /etc/yum.repos.d/CentOS-Epel.repo; Configuration: OptionBinding with id "failovermethod" does not exist
CentOS Linux 8 - AppStream                       73  B/s |  38  B     00:00
Error: Failed to download metadata for repo 'appstream': Cannot prepare internal mirrorlist: No URLs in mirrorlist
```

### Reason

[CentOS Linux 8 had reached the End Of Life (EOL)](https://www.centos.org/centos-linux-eol/) on December 31st, 2021. It means that CentOS 8 will no longer receive development resources from the official CentOS project. After Dec 31st, 2021, if you need to update your CentOS, you need to change the mirrors to [vault.centos.org](https://vault.centos.org/) where they will be archived permanently. Alternatively, you may want to [upgrade to CentOS Stream](https://techglimpse.com/convert-centos8-linux-centosstream/).

### Solution

refer to [Solution to CentOS EOL](https://techglimpse.com/failed-metadata-repo-appstream-centos-8/)

```shell 
# 1. Go to the /etc/yum.repos.d/ directory.
cd /etc/yum.repos.d/
# 2. Run the below commands
sed -i 'sed/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
```

### Linux Basics

- [sed命令](https://www.runoob.com/linux/linux-comm-sed.html)

## 2. 我的docker呢？？？

> [docker 与 podman 的故事：一个方兴未艾，一个异军突起](https://xie.infoq.cn/article/a7254c5d64fcb3be8d6822415)
>
> [Docker 大势已去，Podman 即将崛起](https://segmentfault.com/a/1190000041173604)
>
> [Docker vs Podman](https://www.jianshu.com/p/d80aa43ccf94)
>
> [Podman与Docker有什么不同？](http://dockone.io/article/2434807)

在我满心欢喜`yum install docker -y`安装好docker后，发现我调用docker居然爆出如下的错误：

```shell
# docker
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Error: missing command 'podman COMMAND'
Try 'podman --help' for more information.
```

查了相关资料才知道CentOS已经已用掉docker来作为系统的容器运行时。那么podman和docker的差别到底是什么呢？

- docker会在本地运行一个Docker Engine中的守护进程(docker daemon)来管理自己底下的image，用户通过docker cli连接到dockerd，通过dockerd再来连接到runc(OCI container runtime)。而podman直接与runc交互。

- 但是在软件架构上有一定不同：podman是rootless的并且没有守护进程，解决了docker的单点故障问题等等问题
- 使用上没有本质差别甚至可以`alias docker=podman`

