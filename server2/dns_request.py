import socket

class NS(object):
    def __init__(self, host, port):
        self.server= set()
        self.host = host
        self.port = port
        self.dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dns_sock.connect((self.host, self.port))
        self.BLOCK_SIZE = 1024
        self.status = {}

    def server_connect(self, ip, port):
        print(ip, port)
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((ip, int(port)))
            print("send ping")
            server_sock.send('ping'.encode())
            data = server_sock.recv(self.BLOCK_SIZE).decode()
            print(data)
            server_sock.close()
            if data == "pong":
                self.status[ip+" "+str(port)] = 1
                return True
        except:
            self.status[ip+" "+str(port)] = 0
            server_sock.close()
            return False

        self.status[ip+" "+str(port)] = 0
        server_sock.close()
        return False

    def status_update(self):
        for k, v in self.status.items():
            ip, port = k.split(" ")
            self.server_connect(ip, port)
        return self.status

    def print_status(self):
        print(self.status)

    def get_server_addr(self):
        for k, v in self.status.items():
            if v == 0:
                continue
            data = k.split(" ")
            ip = data[0]
            port = int(data[1])
            yield ip, port
        return None, None
    
    def nslookup(self, name):
        self.dns_sock.send('hello'.encode())
        print("send Hello")
        data = self.dns_sock.recv(self.BLOCK_SIZE).decode()
        print(data)
        if data != 'hello':
            return
        print("Receive: ",data)
        cmd = "nslookup "+name
        self.dns_sock.send(cmd.encode())
        return self.update_status(name)

    def update_status(self, name): 
        data = self.dns_sock.recv(self.BLOCK_SIZE).decode()
        if data == 'done':
            return self.status
        ip, port = data.split(" ")
        ip = ip.strip("''")
        connectable = self.server_connect(ip, port)
        self.dns_sock.send('next'.encode())
        return self.update_status(name)
