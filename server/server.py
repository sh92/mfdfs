import socket, os, sys
import server_middleware as m
print("[*]Enter the IP[*]")
ip = sys.stdin.readline().rstrip()
port = 9803

def server_start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((ip, port))
    except:
        print("[*]Couldn't bind the requested IP[*]")
        sys.exit(0)
    server.listen(1)
    print("[*]Listening to %s : %d[*]" % (ip,port))
    client, addr = server.accept()
    print("[*]Accepted connection form %s : %d[*]" % (addr[0], addr[1]))
    m.cmd_manager(client)

while True:
    server_start()
