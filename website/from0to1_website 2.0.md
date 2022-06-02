# Build my own website

> 感谢[@kiyo5hi](https://github.com/kiyo5hi)提供的技术支持，还给俺讲了很多计网的知识 /贴贴

正在捣鼓[from0to1_website 1.0](./from0_to1_website.md)的时候和kiyo5hi聊了一下。直接改变了我之前所有想要配置的想法。总结一下他的意思就是

- docker更加方便快捷且值得学习，直接在server中只跑一个镜像让自己的服务器环境更干净
- 别使用wodpress, apache...太大了，负担太重了，来点lightweight一点的东西...
- nginx有很多服务我们使用不上的...

这里我准备使用它的配置来部署自己的服务器

- caddy + hoxe...还有什么呢？我也不太知道...

> 等会儿kiyo5hi回家说他帮我搭建博客！然后我自己记笔记，然后rm掉所有东西之后自己reproduce 一边。感觉可以学到很多东西，期待。

---

## prerequisite

搭建一个网站往往需要准备以下几个材料：

- 属于自己的云服务器  --  compulsory

购买云服务器大多都十分昂贵，但是不少大厂的云厂商都提供了校园优惠。我是在 [腾讯云 云+校园](https://cloud.tencent.com/act/campus) 上购买的”轻量应用服务器2核2G“服务器。三年仅仅需要190rmb真的超级划算。

- 属于自己的域名  --  optional

~~当然你可以直接使用你服务器的公网ip来访问你的网站。但是我总觉得那不够酷，也不便于我自己记忆。所以我也是在[腾讯云](https://cloud.tencent.com/act/domainsales)上购买的。选择的域名就是`summer-field.xyz`。至于为什么后缀要选择xyz：第一是我名字的首拼是xy，第二就是腾讯云给的定义`xyz = "幸运者"` ，还蛮酷的哈lol~~ 

昨天和kiyo5hi聊了之后被说xyz的域名太掉价了，果断又买了一个`summer-field.com`的域名...

---

## Set up docker env on debian

### Operate on user instead of root

> 在自己裸服务器中，默认ssh登录的用户是root权限的用户，也就是你对os有所有的权限，但是我们不能习惯于使用root用户来操作服务器，这样会有很多安全隐患，一手抖可能就会造成不可挽回的后果。

debian中使用`useradd`, `adduser`来添加新用户。`adduser`是更底层的`useradd`的wrapper，更加的user friendly。

- 使用`adduser`会提供更多让你配置的信息，例如`password`,`profile info`

同时使用`adduser`命令会为该用户在`/home/`创建属于这个用户自己的用户文件夹，他在这里有write, edit, add/delete file的权限

- 使用`useradd`只会添加一个用户，而不会配置这个用户的相关信息

```shell
$ sudo adduser <your-user-name>
$ sudo usermod -aG sudo <your-user-name> # have the newly created user to have administrative rights
```

为了能够让自己本地主机不使用密码就可以连接到服务器中在本地主机执行如下命令：

```shell
$ ssh-keygen -t rsa # 生成公钥文件id_rsa.pub, 私钥文件id_rsa在~/.ssh目录中
```

在服务器中：

```shell
$ cd # cd to home dir
$ mkdir .ssh # create a .ssh directory
$ cat <your-id_rsa.pub> >> ~/.ssh/authorized_keys 
```

这样以后本地`ssh <username>@<server_ip>`连接到server的自己创建的用户就不需要输入密码了。

### Install Docker

just follow the commands provided in [Install Docker Engine on Debian](https://docs.docker.com/engine/install/debian/)

```shell
# 更新apt-get包管理器，并安装如下包
 sudo apt-get update
 sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
# 添加Docker官方GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# 设置稳定仓库，
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# 安装Docker Engine
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io
# 检查是否安装成功
 docker --version
```

### Install Docker-Compose

```shell
 # Download current stable release of Docker-Compose
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 # 如果官方github镜像太慢可以使用境内的镜像，我这里使用的是daocloud的镜像
 sudo curl -L https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
 # 改变该二进制文件的执行权限
 sudo chmod +x /usr/local/bin/docker-compose
```

-  `uname -s` : Linux
-  `uname -m`: x86_64
- `curl -L, --location`:  Follow redirects
- `curl -o`, --output <file>: Write to file instead of stdout

如果没有报出任何错误那么我们就成功搭建好我们的Docker环境了。

---

## Build Catty Webserver on docker

### [Caddyfile](https://caddyserver.com/docs/caddyfile-tutorial)

```shell
$ mkdir -p /etc/caddy
$ vim Caddyfile
```

Caddyfile:

```json
:8080 {
	root * /srv/website1
	file_server

	header {
		Strict-Transport_Security max-age=31536000;
		Cache-Control max-age=31557600;
	}
}

:8081 {
	root * /srv/website2
	file_server

	header {
		Strict-Transport_Security max-age=31536000;
		Cache-Control max-age=31557600;
	}
}
```



### Permission Denied when connect to Docker Daemon

当我使用`docker ps`时报出一下错误：

```shell
$ docker ps
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json": dial unix /var/run/docker.sock: connect: permission denied

```

原因是：docker进程使用Unix Socket而不是TCP端口。而默认情况下，Unix socket属于root用户，需要root权限才能访问。

解决办法：

1. 使用sudo获取管理员权限，运行docker命令
2. 添加docker group组，将用户添加进去

```shell
$ sudo groupadd docker
groupadd: group 'docker' already exists # 添加docker用户组
$ sudo gpasswd -a $USER docker # 将登陆用户加入到docker用户组中
Adding user field to group docker
$ newgrp docker # 更新用户组
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### Build Container with docker-compose

当然，我们可以手撸命令行来起caddy服务，不过这样太麻烦，且难于管理集群。所以在kiyo5hi的帮助下，学习了docker-compose，并使用docker-compose来起自己的caddy服务。以下是`docker-compose.yml`

```yaml
version: "3"

services:
  caddy:
    image: "caddy:latest" # specify the image
    volumes:
      - "/etc/caddy/Caddyfile:/etc/caddy/Caddyfile" # mount you Caddyfile to container
      - "/home/field/Source/site:/srv" # mount your website file to contiander
      - "/etc/caddy/caddy_data:/data" # for backup
      - "/etc/caddy/caddy_config:/config" # for backup
    ports:
      - "80:80" # HTTP
      - "443:443" # HTTPS
      - "8080:8080" # HTTP
      - "8081:8081" # HTTP

volumes:
    caddy_data:
      external: true
    caddy_config:
```

然后使用

```shell
$ docker-compose up -d
```

就可以把我们的caddy服务器起起来。

> ```shell
> $ docker run -d \
> -v /etc/caddy/Caddyfile:/etc/caddy/Caddfile \
> -v /home/field/Source/site:/srv \
> -v /etc/caddy/caddy_data:/data \
> -v /etc/caddy/caddy_config:/config \
> -p 8080 \
> -p 433:433 \
> -p 8080:8080 \
> -p 8081:8081 \
> caddy:latest
> ```
>
> docker的cmd应该是这样...感兴趣的同学可以自己试一下...

## [Hugo](https://gohugo.io/)



> [How to add and delete user on debian](https://linuxize.com/post/how-to-add-and-delete-users-on-debian-9/)
>
> [How to add/delete user to/from group](https://linuxize.com/post/how-to-add-user-to-group-in-linux/)