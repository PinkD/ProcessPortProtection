import socket
import ssl

from concurrent.futures.thread import ThreadPoolExecutor

import os

from Request import Request
from ExecuteTimer import ExecuteTimer


def parse_request(request):
    if request:
        kvs = request.split("&")
        request = {}
        for kv in kvs:
            k, v = kv.split("=")
            request[k] = v.rstrip()
        return request
    else:
        return None


class ProcessPortProtectionServer:
    # ppp -i [interface] -p [listen port] -pp [protected port] [command]
    response = {
        "HTTP": b'HTTP/1.1 200 OK\r\n\r\n',
        "RAW": b'OK\n'
    }
    BUFFER_SIZE = 1024
    _protect_socket = socket.socket()
    _pool = ThreadPoolExecutor()
    _execute_timer = ExecuteTimer(_pool)

    def _init(self):
        if self.debug:
            print("iptables -t filter -D INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))
            print("iptables -t filter -A INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))
        os.system("iptables -t filter -D INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))
        os.system("iptables -t filter -A INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))
        return True

    def __init__(self, port, interface, protect, key='123', debug=False):
        self.port = port
        self.interface = interface
        self.protect = protect
        self.key = key
        self.debug = debug
        if not self._init():
            raise EnvironmentError("Cannot init")

    def __del__(self): # TODO: delete added rules, may add a list to store
        if self.debug:
            print("iptables -t filter -D INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))
        os.system("iptables -t filter -D INPUT -i %s -p tcp --dport %d -j REJECT" % (self.interface, self.protect))

    def _allow_client(self, request: Request):
        # iptables -t filter -I INPUT -s [client ip] -i [interface] -p tcp --dport [protected port] -j ACCEPT
        if self.debug:
            print("iptables -t filter -D INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
            print("iptables -t filter -A INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
        os.system("iptables -t filter -D INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
        os.system("iptables -t filter -A INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
        print("Verified %s:%d" % request.addr)
        print("+%dh" % request.time)
        self._execute_timer.schedule_count_down(self._timeout_callback, request, self)

    @staticmethod
    def _timeout_callback(self, request: Request):
        if self.debug:
            print("iptables -t filter -D INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
        os.system("iptables -t filter -D INPUT -s %s -i %s -p tcp --dport %d -j ACCEPT" % (request.addr[0], self.interface, self.protect))
        print("Out of date %s:%d" % request.addr)

    def _verify_request(self, request):
        if request:
            data = request.decode()
            if "HTTP" in data:
                param_map = parse_request(data.split("\r\n\r\n")[1])
                type = "HTTP"
            else:
                type = "RAW"
                param_map = parse_request(data)
            verified = False
            deadline = 24
            for k in param_map.keys():
                if k == "key" and param_map[k] == self.key:
                    verified = True
                elif k == "time":
                    try:
                        deadline = int(param_map[k])
                    except ValueError:
                        print("bad time")
                # elif k=="":
            return type, verified, deadline
        else:
            return "", False, 0

    @staticmethod
    def _handle_socket(self, client_socket, client_addr):
        request = client_socket.recv(self.BUFFER_SIZE)
        print("Accept %s:%d" % client_addr)
        (type, verified, deadline) = self._verify_request(request)
        if verified:
            self._allow_client(Request(client_addr, deadline))
            client_socket.send(self.response[type])
        client_socket.close()

    def start(self):
        self._protect_socket.bind(('0.0.0.0', self.port))
        self._protect_socket.listen()
        while True:
            try:
                (client_socket, client_addr) = self._protect_socket.accept()
                client_socket = ssl.wrap_socket(client_socket, certfile='certs/ppp.crt', keyfile='certs/ppp.key', ca_certs='certs/ca.crt', server_side=True)
                self._pool.submit(self._handle_socket, self, client_socket, client_addr)
            except ssl.SSLError as e:
                print(e)
