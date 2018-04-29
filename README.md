# Process Port Protection

Protect a port using `iptables`

It drops the connection to the protected port and starts a daemon to linsten on a port to authorize client, add client to an access list so that client can access to the protected port. 

## Usage

### server

Before you use it, you should generate your own tls cert. Use [gen.sh](certs/gen.sh) to do that.

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

### client

TLS was used in the project, so you can use openssl or curl to request.

#### openssl:

`openssl s_client -connect server_ip:port`

then you input `key=xxx` to authorize.


#### curl

`curl -k https://server_ip:port/ -d "key=xxx"`

### other options

#### time:
- type: integer
- unit: hour
- meaning: available time
- e.g.: time=12 means this authorization will last 12h
- code: `curl -k https://server_ip:port/ -d "key=xxx&time=12"`
