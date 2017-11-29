import socket, os, sys
from subprocess import call
import subprocess


def file_sender(location, client_socket):
    f = open(location, 'r')
    data = f.read()
    print("[*]Sending %s[*]" % location)
    client_socket.sendall(data)
    print("[*]Sent %s[*]" % location)
    f.close()
    client_socket.send("STOP")
    client_socket.recv(4096)


# A file reciver for the reciver
def file_reciver(sv, client):
    f = open(sv, 'a')
    data = client.recv(1024)
    while data:
        f.write(data)
        data = client.recv(1024)
        if "STOP" in data:
            break
    f.write(data[:-4])
    client.send("recived")
    f.close()
    print("[*]Saved %s[*]" % sv)

def folder_sender(location, client_socket):
    os.chdir(location)
    location = os.getcwd()
    no = len(list(os.listdir(location)))
    client_socket.send(str(no))
    print("[*]Preparing to send %d objects[*]" % no)
    res =(client_socket.recv(1024))
    print(res)
    for x in os.listdir(location):
        client_socket.send(x)
        print("[*]Sending %s[*]" % x)
        client_socket.recv(1024)
        # Call the server manager
        server_manager(x, client_socket)
        os.chdir(location)
        print(location)


def folder_reciver(sv, client):
    try:
        os.mkdir(sv)
    except:
        print("[*]File %s already exists can't overwrite[*]" % sv)
        return
    os.chdir(sv)
    location = os.getcwd()
    print(location)
    no = client.recv(1024)
    print ("[*]Preparing to recive %s objects[*]" % no)
    client.send("[*]Ready to recive[*]")
    for x in range(int(no)):
        sv = client.recv(4096)
        print ("Reciving %s" % sv)
        client.send("Recived new object")
    # call the client manager
        client_manager(sv, client)
        os.chdir(location)  # Go to the previous diectory
        print("Saved to %s" % location)


def client_manager(sv, client):
    c = client.recv(4096)
    print(c)
    if c == "DIR":
        folder_reciver(sv, client)
    else:
        file_reciver(sv, client)

def server_manager(location, client_socket):
     if os.path.isdir(location):
        folder_sender(location, client_socket)


def read_file(client_socket, server_root_path, path):
    realpath = os.path.abspath(server_root_path+"/"+path)
    x  = os.system("cat %s > cat.txt"% realpath)
    f = open("cat.txt", "r")
    m = f.readline().split("\n")
    m = m[:-1]
    client_socket.send(str(len(m)).encode())
    ret = client_socket.recv(1024)
    if ret != b'ok':
        return 
    for x in m:
        sys.stdout.write(x)
        sys.stdout.flush()
        client_socket.send(x.encode())
        ret = client_socket.recv(1024)
        if ret == b'ok':
            continue
    os.system("rm cat.txt")


def show_list(client_socket, server_root_path, path):
    realpath = os.path.abspath(server_root_path+"/"+path)
    x  = os.system("ls -l %s > ls.txt"% realpath)
    f = open("ls.txt", "r")
    flist = os.listdir(realpath)
    client_socket.send(str(len(flist)).encode())
    ret = client_socket.recv(1024)
    if ret != b'ok':
        return
    for x in f:
        sys.stdout.write(x)
        sys.stdout.flush()
        client_socket.send(x.encode())
        ret = client_socket.recv(1024)
        if ret == b'ok':
            continue
        else:
            return
    os.system("rm ls.txt")
   

def cmd_manager(client_socket):
    #server_root_path = input("Type server root path")
    server_root_path = os.getcwd()
    if os.path.exists('home')==False:
        os.mkdir('home')
    server_root_path = os.path.join(server_root_path, "home")

    server_root_path = server_root_path
    while True:
       print("")
       command = client_socket.recv(1024).decode()
       cmd = command.split(" ")
       if cmd[0] == 'ls':
           show_list(client_socket, server_root_path, cmd[1] )
       elif cmd[0] == 'cat':
           read_file(client_socket, server_root_path, cmd[1] )
       elif command == 'exit':
           print("Exit")
           break
       else:
           print("Invalid Request")
           break
           
