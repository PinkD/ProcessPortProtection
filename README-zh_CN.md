# Process Port Protection

[简体中文](README-zh_CN.md) | [English](README.md)

该软件使用 `iptables` 来保护一个端口

通过默认丢弃被保护端口的连接，开启另一个端口来授权，将被授权的客户端地址添加进白名单，白名单中客户端即可连接被保护的端口

## 用法

### 服务端

在使用本软件之前，你需要手动生成tls证书，本软件提供了脚本： [gen.sh](certs/gen.sh)

```
usage: main.py [-h] [-v] [-i interface] [-p port] [-pp port] [-k key]
               [-f file]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         show debug information
  -i interface, --interface interface
                        interface
  -p port, --port port  listen port
  -pp port, --protect port
                        port to protect
  -k key, --key key     access key, default is 123
  -f file, --file file  access key file with single line password in it
```

### 客户端

该软件使用了TLS来加密，因此你需要使用 `openssl` 或 `curl` 来进行请求

#### openssl:

`openssl s_client -connect server_ip:port`

然后输入 `key=xxx` 来授权


#### curl

`curl -k https://server_ip:port/ -d "key=xxx"`

### 其他参数

#### time:
- 类型: int
- 单位: 小时
- 意义: 可用时间
- 例: time=12 表示授权可用时间为12小时
- 代码: `curl -k https://server_ip:port/ -d "key=xxx&time=12"`
