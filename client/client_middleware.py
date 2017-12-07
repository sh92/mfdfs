import socket, os, sys
#import paramiko
from uftp import uftp
import time

#TODO DB 연결 STATELESS 상태로 -> 파일들의 정보들을 database에 저장한다.

BLOCK_SIZE = 1024
def udp_download(client_socket, cmd,  fpath, server_ip):
    receiver_port = input('client udp  port : ')
    print(fpath)
    cmd = cmd + " " +receiver_port
    client_socket.send(cmd.encode('utf-8'))
    ret =  client_socket.recv(BLOCK_SIZE).decode()
    if ret[:2] != 'ok':
        print("Fail to receive")
        return
    server_async_port = int(ret[2:])
    receiver_ip = socket.gethostbyname(socket.getfqdn())
    uftp.receive(client_socket, server_ip, server_async_port, receiver_ip, receiver_port, fpath)

def udp_upload(client_socket, cmd,  fpath, server_ip):
    sender_port = input('client udp port : ')
    cmd = cmd + " " + sender_port
    client_socket.send(cmd.encode('utf-8'))
    ret =  client_socket.recv(BLOCK_SIZE).decode()
    print(ret)
    if ret[:2] != 'ok':
        print("Fail to send")
        return
    server_port = int(ret[2:])
    sender_ip = socket.gethostbyname(socket.getfqdn())
    uftp.send(sender_ip, sender_port, server_ip, server_port, fpath)

def get_local_file_list(cmd, client_home):
    x = cmd.split(" ")
    directory = client_home + x[1]
    os.system("ls -l %s" % directory)

def get_file_list(client_socket, cmd):
    client_socket.send(cmd.encode('utf-8'))
    no = client_socket.recv(BLOCK_SIZE)
    client_socket.send(b"ok")
    for x in range(int(no)+1):
       f = client_socket.recv(BLOCK_SIZE).decode()
       sys.stdout.write(f)
       sys.stdout.flush()
       client_socket.send(b"ok")

def remote_open_file(client_socket, cmd, tmp_home, server_ip):
    x = cmd.split(' ')
    fpath = tmp_home+x[1] 
    udp_download(client_socket, "get "+x[1] , fpath, server_ip)
    local_open_file(cmd, tmp_home)
    udp_upload(client_socket, "put "+x[1] , x[1], server_ip)
    local_remove_file("rm "+x[1], tmp_home)

def local_open_file(cmd, client_home):
    x = cmd.split(' ')
    os.system('vi %s'% (client_home+x[1]))

def local_remove_file(cmd, client_home):
    x = cmd.split(' ')
    os.system('rm %s'% (client_home+x[1]))

def read_file(client_socket, cmd):
    client_socket.send(cmd.encode('utf-8'))
    no = client_socket.recv(BLOCK_SIZE)
    client_socket.send(b"ok")
    for x in range(int(no)):
       f = client_socket.recv(BLOCK_SIZE).decode()
       sys.stdout.write(f)
       sys.stdout.flush()
       client_socket.send(b"ok")

def cmd_manager(client_socket, server_ip, server_port):
    client_home = os.getcwd()+'/home/'
    tmp_home = os.getcwd()+'/tmp/'
    while True:
        print()
        print("[*] Type '?' to get information [*]")
        command = input(">>")

        cmd_list = command.split(" ")
        cmd = cmd_list[0]
        print("")
        if  cmd =="?":
            print("[-] ls < path >: list of files in remote directory")
            print("[-] lsl < path >: list of files in local directory")
            print("[-] put < loacal file > : put a lacal file to a remote file")
            print("[-] get < remote file > : get a remote file")
            print("[-] cat < path >  : read a remote file")
            print("[-] vi < remote file > : open a remote file")
            print("[-] vil < local file > : open a local file")
            #print("[-] rm < remote file > : remove a remote file")
            print("[-] rml < local file > : remove a local file")
            #print("[-] scp < local file > < remote file > : copy from local file to remote file")
            #print("[-] pwd < remote path > : get remote path")
            #print("[-] mkdir < remote directory > : create remote directory")
            #print("[-] cd < remote path > : change directory")
            #print("[-] syn : syncronize server")
            print("[-] exit ")
        elif cmd == 'ls':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            get_file_list(client_socket, command)
        elif cmd == 'lsl':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            get_local_file_list(command, client_home)
        elif cmd == 'put':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            udp_upload(client_socket, command, client_home + cmd_list[1], server_ip)
        elif cmd == 'get':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            udp_download(client_socket, command, cmd_list[1] , server_ip)
        elif cmd == 'cat':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            read_file(client_socket, command)
        elif cmd == 'vi':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            remote_open_file(client_socket, command, tmp_home, server_ip)
        elif cmd == 'vil':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            local_open_file(command, client_home)
        elif cmd == 'rml':
            if len(cmd_list) != 2:
                print("Invalid Argument")
                continue
            local_remove_file(command, client_home)
        elif cmd == "exit":
            if len(cmd_list) != 1:
                print("Invalid Argument")
                continue
            client_socket.send(b"exit")
            break
        else:
            print("[*]Invalid Command : %s" % command)
