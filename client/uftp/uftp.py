import os
import socket
import sys
import time


def receive(client_socket, sender_ip, sender_port, receiver_ip, receiver_port, fpath, buffer_size=1024):
    print("ready for receive... ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    receiver_port = int(receiver_port)
    sock.bind((receiver_ip, receiver_port))
    client_socket.send("ok".encode())
    try:
        filesize, addr = sock.recvfrom(buffer_size)
        filesize = filesize.decode()
        print("File Size: ", filesize)
        size = 0
        remain= int(filesize)
        start_time = time.time()
        with open(fpath, "w") as f:
            while True:
                if remain >= buffer_size:
                    fileInfo , addr = sock.recvfrom(buffer_size)
                    fileInfo = fileInfo.decode()
                    f.write(fileInfo)
                    remain -=buffer_size
                    size += buffer_size
                    print(size ,"/", filesize ," (currentsize/totalsize) ,", round((100.00 *size/int(filesize)),2) ,"%")
                else:
                    fileInfo , addr = sock.recvfrom(remain)
                    fileInfo = fileInfo.decode()
                    f.write(fileInfo)
                    size+=remain
                    print(size ,"/", filesize ," (currentsize/totalsize) ,", round((100.00 *size/int(filesize)),2) ,"%")
                    print("Completed ....")
                    break
        end_time = time.time()
        print("Time elapsed : ", end_time - start_time)
    except socket.error as e:
        print(e)
        sys.exit()

def send(sender_ip, sender_port, receiver_ip, receiver_port, fpath, buffer_size=1024):
    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    sock.settimeout(10)
    size=0
    filesize = os.path.getsize(fpath) 
    remain = filesize
    receiver_port = int(receiver_port)
    print("FileSize : ", filesize)
    sock.sendto(str(filesize).encode(),(receiver_ip, receiver_port))
    time.sleep(1/10.0)
    start_time = time.time()
    try:
        with open(fpath, 'rb') as f:
            while True:
                if remain >= buffer_size:
                    remain -=buffer_size
                    read_data = f.read(buffer_size)
                    size += buffer_size
                    print(size , "/",filesize , "(Currentsize/Totalsize) , ", round((100.00 * size/int(filesize)),2), "%")
                    sock.sendto(read_data,(receiver_ip, receiver_port))
                    time.sleep(1/10.0)
                else:
                    size+=remain
                    read_data = f.read(remain)
                    print(size , "/",filesize , "(Currentsize/Totalsize) , ", round((100.00 * size/int(filesize)),2), "%")
                    sock.sendto(read_data, (receiver_ip, receiver_port))
                    time.sleep(1/10.0)
                    print("Completed ...")
                    break

        end_time = time.time()
        print("Time elapsed : ", end_time - start_time)
    except socket.error as e:
        print(e)
        sys.exit()
