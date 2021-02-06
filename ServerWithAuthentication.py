import socket,hashlib,threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 1234
s.bind((host,port))
ip_list = []
conn_list = []
print(f"\n[+] Server hosted on IP: {host}")
print(f"[+] Server hosted on Port: {port}")
print("\n[+] Server is Up And Running.........\n")
try:
    checker = open('username_passwords.txt', 'r')
except:
    checker = open('username_passwords.txt','w')
def listener():
    while True:
        try:
            s.listen(1)
            conn, ip = s.accept()
            if ip[0] in ip_list:
                message = "You cannot have more than 1 session at a time!".encode('utf-8')
                conn.send(message)
                conn.close()
            else:
                print(f"[+] {ip[0]} Has Joined the Server.")
            ip_list.append(ip[0])
            conn_list.append(conn)
        except:
            pass
def recv():
    while True:
        for conn in conn_list:
            try:
                msg = conn.recv(1024).decode('utf-8')
                print(f"[+] Message From Conn {conn}: {msg}")
                if msg.startswith('!login'):
                    file = open("username_passwords.txt",'r')
                    msg = msg.split()
                    try:
                        username = msg[1]
                        password = msg[2]
                    except:
                        error_msg = 'Invalid Arguements!\nUsage: !login <username> <password>'.encode('utf-8')
                        conn.send(error_msg)
                    file_contents = file.readlines()
                    file.close()
                    flag = 0
                    for line in file_contents:
                        if username in line:
                            info = line
                            flag = 1
                            break
                        else:
                            pass
                    if flag == 0:
                        error_msg = 'Your Username Does Not Exist! Try Registering.'.encode('utf-8')
                        conn.send(error_msg)
                    else:
                        info = info.split()
                        passw = info[1]
                        hashed_pass = hashlib.md5(password.encode()).hexdigest()
                        if passw.strip() == hashed_pass.strip():
                            msg = f'Password Accepted! Welcome {username}.'.encode('utf-8')
                            conn.send(msg)
                        else:
                            if flag == 1:
                                error_msg = 'Password Not Accepted!'.encode('utf-8')
                                conn.send(error_msg)
                            else:
                                pass
                elif msg.startswith('!register'):
                    stop = False
                    msg = msg.split()
                    flag = 0
                    try:
                        new_user = msg[1]
                        new_pass = msg[2]
                        flag = 1
                    except:
                        error_msg = 'Invalid Arguements!\nUsage: !register <username> <password>'.encode('utf-8')
                        conn.send(error_msg)
                    file = open("username_passwords.txt",'r')
                    file_contents = file.readlines()
                    file.close()
                    for line in file_contents:
                        if new_user in line:
                            error_msg = 'The Username is taken! Try using another.'.encode()
                            conn.send(error_msg)
                            stop = True
                            break
                        else:
                            pass
                    if not stop:
                        file = open("username_passwords.txt", "w")
                        new_pass = hashlib.md5(new_pass.encode()).hexdigest()
                        file_contents.extend(f'\n{new_user} {new_pass}')
                        file.writelines(file_contents)
                        file.close()
                        if flag == 1:
                            msg = f"Successfully registered. Welcome, {new_user}!".encode('utf-8')
                            conn.send(msg)
                elif msg.startswith('!reregister'):
                    flag = 0
                    msg = msg.split()
                    try:
                        username = msg[1]
                        old_pass = msg[2]
                        new_pass = msg[3]
                    except:
                        error_msg = 'Invalid Arguements!\nUsage: !register <username> <old_password> <new_password>'.encode('utf-8')
                        conn.send(error_msg)
                    file = open('username_passwords.txt','r')
                    file_contents = file.readlines()
                    file.close()
                    item = 0
                    for line in file_contents:
                        if username in line:
                            info = line
                            break
                        else:
                            pass
                        item += 1
                    info = info.split()
                    password = info[1]
                    old_pass = hashlib.md5(old_pass.encode()).hexdigest()
                    if old_pass == password:
                        flag = 1
                    else:
                        flag = 0
                    if flag == 1:
                        password = new_pass
                        new_pass = hashlib.md5(new_pass.encode()).hexdigest()
                        file_contents.remove(file_contents[item])
                        file_contents.extend(f'\n{username} {new_pass}')
                        file.close()
                        file = open('username_passwords.txt','w')
                        file.writelines(file_contents)
                        msg = f'Hello {username}, you have changed your password to: {password}'.encode()
                        conn.send(msg)
            except:
                pass
def conn_checker():
    while True:
        for conn in conn_list:
            try:
                msg = "".encode('utf=8')
                conn.send(msg)
            except:
                item = 0
                for ip in ip_list:
                    if ip in str(conn):
                        print(f"[+] {ip} Is Offline.")
                        ip_list.remove(ip_list[item])
                        conn.close()
                    else:
                        pass
                    item += 1
listen = threading.Thread(target=listener)
listen.start()
recieve = threading.Thread(target=recv)
recieve.start()
handler = threading.Thread(target=conn_checker)
handler.start()
