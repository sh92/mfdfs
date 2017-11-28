import paramiko

#ip = '172.17.0.2'
ip = '183.107.51.103'
port = 22
username = 'lsh'
password = '123'

def get_file_list(ip,port, user, pwd):
    print("start")
    ssh= paramiko.SSHClient()
    print("?")
    ssh.load_system_host_keys()
    print("?2")
    ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    print("?3")
    ssh.connect(ip, port=port, username=user, password=pwd)
    print("?4")
    print("connect")
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    print("stdout", stdout.readlines())
    ftp = ssh.open_sftp()
    files = ftp.listdir()
    print(files)

get_file_list(ip, port, username, password)
