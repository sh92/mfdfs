import socket, os, sys
import paramiko

def put_file(machinename, username, dirname, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machinename, username=username)
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(dirname)
    except IOError:
        pass
    f = sftp.open(dirname + '/' + filename, 'w')
    f.write(data)
    f.close()
    ssh.close()

def get_file_list(client_socket, cmd):
    client_socket.send(cmd.encode('utf-8'))
    no = client_socket.recv(1024)
    client_socket.send(b"ok")
    for x in range(int(no)+1):
       f = client_socket.recv(1024).decode()
       sys.stdout.write(f)
       sys.stdout.flush()
       client_socket.send(b"ok")

def write_file(client_socket, cmd):
    pass

def read_file(client_socket, cmd):
    pass

def cmd_manager(client_socket):
    while True:
        print()
        print("[*] Type '?' to get information [*]")
        command = input(">>")

        cmd_list = command.split(" ")
        cmd = cmd_list[0]
        if  cmd =="?":
            print("[-] ls < path >: list file in remote directory")
            print("[-] lsl < path >: list file in local directory")
            print("[-] cat < path >  : read remote file")
            print("[-] put < local file > < remote file > : save file")
            print("[-] get < remote file > : get remote file")
            print("[-] pwd < remote path > : get remote path")
            print("[-] mkdir < remote directory > : create remote directory")
            print("[-] cd < remote path > : change directory")
            print("[-] syn : syncronize server")
            print("[-] exit ")
        elif cmd == 'ls':
            get_file_list(client_socket, command)
        elif cmd == 'cd':
            write_file(client_socket, command)
        elif cmd == 'cat':
            read_file(client_socket, command)
        elif cmd == 'pwd':
            pass
        elif cmd == "exit":
            break
        else:
            print("[*]Invalid Argument: %s" % command)
