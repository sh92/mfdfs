import socket, os, sys
from subprocess import call
import subprocess
from uftp import uftp
import time
import dns_request as dns

BLOCK_SIZE = 1024

DNS_SERVER_IP = ""
DNS_SERVER_PORT = 6000
domain = "www.mysite.com"

def udp_receive(client_socket, fpath, server_ip):
    uftp.receive(client_socket, server_ip, fpath)

def udp_send(fpath, client_ip, client_port):
    uftp.send(fpath, client_ip, client_port)

def read_file(client_socket, server_root_path, path):
    realpath = os.path.abspath(server_root_path+"/"+path)
    x = os.system("cat %s > cat.txt"% realpath)
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
    if os.path.exists(path) == False:
        print("Invalid path")
        client_socket.send("Invalid".encode())
        return False
    realpath = os.path.abspath(server_root_path+"/"+path)
    x = os.system("ls -l %s > ls.txt"% realpath)
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

def syncroniztion(client_socket, server_root_path, cmd, server_ip, server_port):
    udp_receive(client_socket, server_root_path+cmd[1], server_ip)

    ssh_id = 'id'
    ssh_password = '1234'
    ip = 'ip'
    start = time.time()
    os.system('sshpass -p '+ssh_password+' ./bsync -i /home/backup '+ssh_id+'@'+ip+':/home/backup')
    end = time.time()
    print("Time elapsed : ", end- start)
    ''' #nameserver
    ns = dns.NS(DNS_SERVER_IP, DNS_SERVER_PORT)
    status_dict = ns.nslookup(domain)
    for ip, port in ns.get_server_addr():
        if ip == server_ip and port == server_port:
            continue
        print(ip, port)
        print("Syncronization")
        ssh_id = input("ssh ID")
        ssh_password = input("Password: ")
        os.system('sshpass -p '+ssh_password+' ./bsync -i /home/backup '+ssh_id+'@'+ip+':/home/backup')
    '''


def cmd_manager(client_socket, server_ip, server_port):
    server_root_path = '/home/backup/'
    '''
    server_root_path = os.getcwd()
    if os.path.exists('home')==False:
        os.mkdir('home')
    server_root_path = os.path.join(server_root_path, "home")+"/"
    '''  
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
           udp_send( server_root_path+cmd[1], cmd[2], cmd[3])
       elif cmd[0] == 'put':
           #udp_receive(client_socket, server_root_path+cmd[1], server_ip)
           syncroniztion(client_socket, server_root_path, cmd, server_ip, server_port)
       elif command == 'exit':
           print("Exit")
           break
       else:
           print("Invalid Request")
           break
           
