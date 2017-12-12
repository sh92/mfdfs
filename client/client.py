import socket, os, sys
import client_middleware as m
import dns_request as dns

#TODO IMPLEMENTE NAME SERVER LATER
DNS_SERVER_IP = '168.188.129.216'
DNS_SERVER_PORT = 6000
domain = 'www.mysite.com'


if __name__ == "__main__":
    ns = dns.NS(DNS_SERVER_IP, DNS_SERVER_PORT)
    status_dict = []
    isFirst = True
    status_dict = ns.nslookup(domain)
    print(status_dict)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(600)
    while True:
        try:
            if isFirst == False:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                status_dict = ns.status_update()
            else:
                isFirst = False

            for ip, port in ns.get_server_addr():
                if ip == None:
                    print("It is not availabe to connect Server") 
                    client.close()
                    exit(1)
                try:
                    client.connect((ip, port))
                    print("Wating ... ")
                    break
                except:
                    print("Port is already in use")
                    continue
            try:
                client.send("hello".encode())
                msg = client.recv(4096).decode()
                print(msg)
                if msg != 'hello':
                    print("Wrong Connect")
                    continue
                print("Connected")
                m.cmd_manager(client, ip, port)
                client.close()
                exit(1)
            except:
                client.close()
                continue
        except KeyboardInterrupt:
            print("Bye")
            break
            sys.exit()
