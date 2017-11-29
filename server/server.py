import socket, os, sys
import select
import server_middleware as m

def broadcast_data (sock, message ):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

    
if __name__ == "__main__":
    RECV_BUFFER = 4096
    CONNECTION_LIST = []
    ip = input("Server IP : ")
    port= int(input("Server PORT : "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((ip, port))
    except:
        print("[*]Couldn't bind the requested IP[*]")
        sys.exit(0)
    server_socket.listen(1)
    CONNECTION_LIST.append(server_socket)
    print("[*]Listening to %s : %d[*]" % (ip,port))
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
           if sock == server_socket:
                sockfd, addr = server_socket.accept()
                msg = sockfd.recv(RECV_BUFFER)
                if msg != b'connect':
                    print("Disconnect")
                    sockfd.close()
                    continue
                sockfd.send(b'connect')
                CONNECTION_LIST.append(sockfd)
                print("[*]Accepted connection form %s : %d[*]" % (addr[0], addr[1]))
                m.cmd_manager(sockfd)
                broadcast_data(sockfd, "Client (%s, %s) is offline" % addr)
                sockfd.close()
                CONNECTION_LIST.remove(sockfd)
           else:
                #try:
                #    data = sock.recv(RECV_BUFFER)
                #    if data:
                #       broadcast_data(sock, data)
                #except:
                broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                print("Client (%s, %s) is offline" % addr)
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue

