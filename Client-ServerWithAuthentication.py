import socket, threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        ip = input("[+] Enter the IP to connect to: ")
        port = int(input("[+] Enter the Port to connect to: "))
        s.connect((ip, port))
        break
    except:
        print("\n[+] Invalid IP or Port.\n")
commands_list = ['!register','!login']
print("[+] Connected to the server.......\n")
def instruct():
    while True:
        instruction = input("[+] What is the instruction: ")
        try:
            insplit = instruction.split()
            if insplit[0] in commands_list:
                try:
                    s.send(instruction.encode('utf-8'))
                except:
                    print("[+] Your Connection has been Terminated by the host.")
                    input("\n[+] Press 'enter' to exit.")
                    quit()
        except:
            pass
def recv():
    while True:
        try:
            msg = s.recv(1024).decode('utf-8')
            if msg == "":
                pass
            else:
                print(f"\n[+] Msg from Serv: {msg}")
        except:
            pass
sender = threading.Thread(target=instruct)
reciever = threading.Thread(target=recv)
sender.start()
reciever.start()
