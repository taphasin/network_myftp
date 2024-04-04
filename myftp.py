import socket
import random

isconnect = False

while True:
    line = input('ftp> ').strip()
    args = line.split()
    command = args[0]

    if command == 'open':
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server = args[1]
        except:
            server = input("To ")
        print(f"Connected to {server}")
        clientSocket.connect((f"{server}", 21))
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        print("202 UTF8 mode is always enabled. No need to send this command")

        user = input(f"User ({server}:(none)): ")
        clientSocket.send(f"USER {user}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        password = input("Password:")
        clientSocket.send(f"PASS {password}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        isconnect = True

    if (isconnect == False and command in ['ascii','binary','cd','close','delete','disconnect','get','ls','open','put','pwd','rename','user']):
        print("Not connected.")

    elif (command == 'quit' or command == 'bye'):
        try:
            clientSocket.send("QUIT\r\n".encode())
            resp = clientSocket.recv(1024)
            print(resp.decode(), end = "")
            clientSocket.close()
            isconnect = False
            break
        except:
            break

    elif (command == 'disconnect' or command == 'close'):
        clientSocket.send("QUIT\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        clientSocket.close()  
        isconnect = False  
    



    elif command == 'ls':

        data_port = random.randint(1025, 65535)
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        clientSocket.send("NLST\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(("127.0.0.1", int(data_port)))
        dataSocket.listen(5)
        dataPort, a = dataSocket.accept()

        while True:
            resp = dataPort.recv(1024)
            print(resp.decode(), end = "")
                 
            if not resp:
                break

        dataSocket.close()
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

    elif command == "ascii":
        clientSocket.send("TYPE A\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        
    elif command == "binary":
        clientSocket.send("TYPE I\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        
    elif command == "cd":
        try: 
            path = args[1]         
        except:
            path = input("Remote directory")

        clientSocket.send(f"CWD {path} \r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        
    elif command == "pwd":
        clientSocket.send("XPWD\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

    elif command == "rename":
        try: 
            old = args[1]       
        except:
            old = input("From name ")
        
        try:
            to = args[2]
        except:
            to = input("To name ")

        clientSocket.send(f"RNFR {old}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        clientSocket.send(f"RNTO {to}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end ="")

    elif command == "delete":
        try: 
            file = args[1]         
        except:
            file = input("Remote file ")
        clientSocket.send(f"DELE {file}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

    elif command == "get":
        data_port = random.randint(1025, 65535)
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        try: 
            remotefile = args[1]         
        except:
            remotefile = input("Remote file ")

        clientSocket.send(f"RETR {remotefile}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        resp_sp = resp.decode()
        resp_sp = resp_sp.split()
        if resp_sp[0] == "550":
            print("in 53")
            pass
        else:
            dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataSocket.bind(("127.0.0.1", int(data_port)))
            dataSocket.listen(5)
            dataPort, a = dataSocket.accept()
            resp = dataPort.recv(1024)

            try:
                localfile = args[2]
            except:
                try:
                    localfile = args[1]
                except:
                    localfile = input("Local file ")


            with open(localfile, 'wb') as file:
                file.write(resp)


            dataPort.close()
            data = clientSocket.recv(2048)
            print(data.decode(), end = "")


    elif command == "put":
        try:
            put_file = args[1]
        except:
            put_file = input("Local file ")
        try:
            file = open(f"{put_file}", "rb")

            data_port = random.randint(1025, 65535)
            open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"

            clientSocket.send(f"PORT {open_con}\r\n".encode())
            resp = clientSocket.recv(1024)
            print(resp.decode(), end = "")

            clientSocket.send(f"STOR {put_file}\r\n".encode())
            resp = clientSocket.recv(1024)
            print(resp.decode(), end = "")

            dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataSocket.bind(("127.0.0.1", int(data_port)))
            dataSocket.listen(5)
            dataPort, a = dataSocket.accept()
            print("has come this state")

            data = file.read(1024)
            dataPort.send(data)

            dataPort.close()
            data = clientSocket.recv(2048)
            print(data.decode(), end = "")

        except FileNotFoundError:
            print(f"{put_file}: File not found")
            
            

    elif command == "user":
        try:
            username = args[1]
        except:
            username = input("Username ")
            if username == None:
                print("Usage: user username [password] [account]")
                break

        clientSocket.send(f"USER {username}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        try:
            password = args[2]
        except:
            password = input("Password: ")

        clientSocket.send(f"PASS {password}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

    
    else:
        print("Invalid command.")


