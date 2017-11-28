import socket, os, sys
import client_middleware as m
print("[*]Enter server the IP[*]")
ip = sys.stdin.readline().rstrip()
port = 9803

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
    except:
        print("[*]Coudn't connect to the requested server [*]")
        exit(1)
    print("Connected")
    m.cmd_manager(client)
