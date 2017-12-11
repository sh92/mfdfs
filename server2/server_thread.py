import socket, os, sys
import threading
import server_middleware as m
import threading

RECV_BUFFER = 4096

class ThreadedServer(object):
    def __init__(self, host, port):
        self.connections = set()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(600)
            self.connections.add((client, address))
            msg = client.recv(RECV_BUFFER).decode()
            print(msg)
            if msg == 'ping':
                client.send("pong".encode())
                continue
            if msg != 'hello':
                print("Disconnect")
                client.close()
                continue
            client.send('hello'.encode())
            print("[*]Accepted connection form %s : %d[*]" % (address[0], address[1]))
            threading.Thread(target = m.cmd_manager, args = (client, self.host, self.port)).start()

    
if __name__ == "__main__":
    ip = '127.0.0.1' #input("Server IP : ")
    port = 8200 #int(input("Server PORT : "))
    print("[*]Listening to %s : %d[*]" % (ip, port))
    try:
    	ThreadedServer(ip, int(port)).listen()
    except:
        print("[*]Couldn't bind the requested IP[*]")
        sys.exit(0)
