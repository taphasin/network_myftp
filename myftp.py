import socket
import random


while True:
    line = input('ftp> ').strip()
    args = line.split()

    command = args[0]
    if (command == 'quit' or command == 'bye'):
        clientSocket.send("QUIT\r\n")
        resp = clientSocket.recv(1024)
        print(resp.decode())
        clientSocket.close()
        break

    elif command == 'open':
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("127.0.0.1", 21))
        resp = clientSocket.recv(1024)
        print(resp.decode())

        # user = input(f"User ({args[1]}:(none)): ")
        # print(user)
        clientSocket.send("USER bob\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        # password = input("Password:")
        clientSocket.send("PASS 12345\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

    elif (command == 'disconnect' or command == 'close'):
        clientSocket.send("QUIT\r\n")
        resp = clientSocket.recv(1024)
        print(resp.decode())
        clientSocket.close()
        


    elif command == 'ls':

        data_port = random.randint(1025, 65535)
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        clientSocket.send("NLST\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end="")

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(("127.0.0.1", int(data_port)))
        dataSocket.listen(5)
        dataPort, a = dataSocket.accept()

        while True:
            resp = dataPort.recv(1024)
            print(resp.decode(), end="")
                 
            if not resp:
                break

        dataSocket.close()
        resp = clientSocket.recv(1024)
        print(resp.decode(), end="")

    elif command == "ascii":
        clientSocket.send("TYPE A\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())
        
    elif command == "binary":
        clientSocket.send("TYPE I\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())
        
    elif command == "cd":
        clientSocket.send(f"CWD {args[1]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())
        
    elif command == "pwd":
        clientSocket.send("XPWD\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

    elif command == "rename":
        clientSocket.send(f"RNFR {args[1]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        clientSocket.send(f"RNTO {args[2]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

    elif command == "delete":
        clientSocket.send(f"DELE {args[1]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

    elif command == "get":
        data_port = random.randint(1025, 65535)
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"
        print(type(data_port))

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        clientSocket.send(f"RETR {args[1]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(("127.0.0.1", int(data_port)))
        dataSocket.listen(5)
        dataPort, a = dataSocket.accept()

        resp = dataPort.recv(1024)
        print("Data received on data socket:", resp.decode())     
        with open(args[1], 'wb') as file:
            file.write(resp)


        dataPort.close()
        data = clientSocket.recv(2048)
        print(data.decode())


    elif command == "put":
        data_port = random.randint(1025, 65535)
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"
        print(type(data_port))

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        clientSocket.send(f"STOR {args[1]}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(("127.0.0.1", int(data_port)))
        dataSocket.listen(5)
        dataPort, a = dataSocket.accept()

        with open("rebex.txt", 'rb') as file:
            data = file.read(1024)
            dataPort.send(data)

        dataPort.close()
        data = clientSocket.recv(2048)
        print(data.decode())

    elif command == "user":
        if not args[1]:
            user = input("Username: ")
            if not user:
                print("Usage: user username [password] [account]")
                break

        clientSocket.send(f"USER {args[1]}")
        resp = clientSocket.recv(1024)
        print(resp.decode())


        if not args[2]:
            password = input("Password: ")
        
        clientSocket.send(f"PASS {args[2]}")
        resp = clientSocket.recv(1024)
        print(resp.decode())

    
    else:
        print("Invalid command.")