import socket, os, sys
import threading
import redis

RECV_BUFFER = 4096

DNS_SERVER_IP = '127.0.0.1'
DNS_SERVER_PORT = 6000

DNS = {}
# Reverse Oder
DNS['www.mysite.com'] = [['127.0.0.1', 8200], ['127.0.0.1',9200]]

class NameServer(object):
    def __init__(self, host, port):
        self.connections = set()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.rs =  redis.Redis(host='localhost', port=6379)

    def listen(self):
        self.dns_setup('www.mysite.com')
        self.sock.listen(10)

        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            self.connections.add((client,address))
            msg = client.recv(RECV_BUFFER).decode()
            if msg != 'hello':
               print("Disconnect")
               client.close()
               continue
            client.send('hello'.encode())
            print("[*]Accepted connection form %s : %d[*]" % (address[0], address[1]))
            self.handler(client)

    def handler(self, client):
        print("Wating client request")
        while True:
            data = client.recv(RECV_BUFFER).decode()
            print(data)
            dlist = data.split(" ")
            cmd = dlist[0] 
            if cmd == 'nslookup':
                name = dlist[1]
                print(name)
                for ip, port in self.nslookup(name):
                    print(ip, port)
                    data = ip+" "+port
                    client.send(data.encode())
                    msg = client.recv(RECV_BUFFER).decode()
                    if msg =='next':
                        continue
                client.send("done".encode())
                break

    def server_ping_report(self, client, name):
        for ip, port in self.nslookup(name):
            print(ip, port)

    def dns_setup(self, name):
        result = self.rs.lrange(name, 0, -1)
        print(result)
        if result == []:
            for x in DNS[name]:
                self.rs.lpush(name, x)
        else:
            while result != []:
                self.rs.lpop(name)
                result = self.rs.lrange(name, 0, -1)
            print("update dns")
            for x in DNS[name]:
                self.rs.lpush(name, x)

    def nslookup(self, name):
        result = self.rs.lrange(name, 0, -1)
        for x in result:
            x = x.decode()
            x = x.strip('[]')
            x = x.split(', ')
            ip = x[0]
            port = x[1]
            yield ip, port

if __name__ == '__main__':
    print("[*]Listening to %s : %d[*]" % (DNS_SERVER_IP, DNS_SERVER_PORT))
    NameServer(DNS_SERVER_IP,DNS_SERVER_PORT).listen()
