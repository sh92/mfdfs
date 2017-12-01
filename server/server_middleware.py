import socket, os, sys
from subprocess import call
import subprocess
from uftp import uftp
import time

BLOCK_SIZE = 1024
server_another_port = 8000

def udp_receive(client_socket, fpath, server_ip, server_port, client_port):
    sender_ip = socket.gethostbyname(socket.getfqdn())
    sender_port = client_port
    client_socket.send(('ok'+str(server_another_port)).encode())
    print("Wating udp....")
    print(fpath)
    uftp.receive(client_socket, sender_ip, server_another_port, server_ip, server_another_port, fpath)

def udp_send(client_socket, fpath, server_ip, server_port, client_port):
    receiver_ip = socket.gethostbyname(socket.getfqdn())
    receiver_port = client_port
    client_socket.send(('ok'+str(server_another_port)).encode())
    print("Wating udp....")
    ret = client_socket.recv(BLOCK_SIZE).decode()
    print(ret)
    if ret != 'ok':
        print("Fail to send")
        return
    time.sleep(2)
    uftp.send(server_ip, server_port, receiver_ip, receiver_port, fpath)
    print("Finsh to send")


def read_file(client_socket, server_root_path, path):
    realpath = os.path.abspath(server_root_path+"/"+path)
    x  = os.system("cat %s > cat.txt"% realpath)
    fpath = './cat.txt'
    f = open(fpath, "r")
    fsize = os.path.getsize(fpath)
    if fsize%BLOCK_SIZE == 0:
        num = int(fsize/BLOCK_SIZE)
    else:
        num = int(fsize/BLOCK_SIZE) + 1
    client_socket.send(str(num).encode())
    ret = client_socket.recv(BLOCK_SIZE)
    if ret != b'ok':
        return
    while True:
        x = f.read(BLOCK_SIZE)
        if x == '':
            break
        sys.stdout.write(x)
        sys.stdout.flush()
        client_socket.send(x.encode())
        ret = client_socket.recv(BLOCK_SIZE)
        if ret == b'ok':
            continue
    os.system("rm cat.txt")


def show_list(client_socket, server_root_path, path):
    realpath = os.path.abspath(server_root_path+"/"+path)
    x  = os.system("ls -l %s > ls.txt"% realpath)
    f = open("ls.txt", "r")
    flist = os.listdir(realpath)
    client_socket.send(str(len(flist)).encode())
    ret = client_socket.recv(BLOCK_SIZE)
    if ret != b'ok':
        return
    for x in f:
        sys.stdout.write(x)
        sys.stdout.flush()
        client_socket.send(x.encode())
        ret = client_socket.recv(BLOCK_SIZE)
        if ret == b'ok':
            continue
        else:
            return
    os.system("rm ls.txt")
   

def cmd_manager(client_socket, server_ip, server_port):
    #server_root_path = input("Type server root path")
    server_root_path = os.getcwd()
    if os.path.exists('home')==False:
        os.mkdir('home')
    server_root_path = os.path.join(server_root_path, "home")+"/"

    server_root_path = server_root_path
    while True:
       print("")
       command = client_socket.recv(1024).decode()
       print(command)
       cmd = command.split(" ")
       if cmd[0] == 'ls':
           show_list(client_socket, server_root_path, cmd[1] )
       elif cmd[0] == 'cat':
           read_file(client_socket, server_root_path, cmd[1] )
       elif cmd[0] == 'get':
           udp_send(client_socket, server_root_path+cmd[1], server_ip, server_port, cmd[2])
       elif cmd[0] == 'put':
           udp_receive(client_socket,  server_root_path+cmd[1], server_ip, server_port, cmd[2])
       elif command == 'exit':
           print("Exit")
           break
       else:
           print("Invalid Request")
           break
           
