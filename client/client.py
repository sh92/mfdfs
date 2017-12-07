import socket, os, sys
import client_middleware as m

#TODO IMPLEMENTE NAME SERVER LATER
DNS_SERVER_IP = '127.0.0.1'
DNS_SERVER_PORT = 6000

DNS={}
server_ip_list = ['127.0.0.1','127.0.0.1']
server_port_list = [9000,8000]
DNS['server'] = server_ip_list

print("[*]Enter server the IP[*]")
primary_server_ip = sys.stdin.readline().rstrip() #server_ip_list[0]
print("[*]Enter server the PORT[*]")
port = int(sys.stdin.readline().rstrip()) #server_port_list[0]

IS_SERVER = False
for s_ip in DNS['server']:
    if primary_server_ip == s_ip:
        IS_SERVER = True
        break

if IS_SERVER == False:
    exit(1)

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.settimeout(2)
    try:
        client.connect((primary_server_ip , port))
        print("Wating ... ")
        client.send(b"connect")
        msg = client.recv(4096)
        if msg != b'connect':
            print("Wrong Connect")
            client.close()
            exit(1)
        print("Connected")
        m.cmd_manager(client, primary_server_ip, port)
    except:
        print("[*]Coudn't connect to the requested primary server [*]")
        try:
            print("[*]Try to connect to the secondary server [*]")
            print("[*]Enter the secondary server IP [*]")
            seconday_server_ip = sys.stdin.readline().rstrip() #server_ip_list[0]
            print("[*]Enter the secondary server PORT [*]")
            seconday_server_port = sys.stdin.readline().rstrip() #server_port_list[0]
            client.connect((seconday_server_ip , seconday_server_port))
            m.cmd_manager(client, seconday_server_ip, seconday_server_port)
        except:
            exit(1)
