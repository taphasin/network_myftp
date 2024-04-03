import socket
import random


while True:
    line = input('ftp> ').strip()
    args = line.split()

    command = args[0]
    print(command)
    if command == 'quit':
        break
    elif command == 'bye':
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

    elif command == 'disconnect':
        clientSocket.close()
        print('disconnect')


    elif command == 'ls':

        data_port = random.randint(1025, 65535)  # Choose a random port number
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"
        print(type(data_port))

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        clientSocket.send("NLST\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind(("127.0.0.1", int(data_port)))
        dataSocket.listen(5)
        dataPort, a = dataSocket.accept()

        while True:
            resp = dataPort.recv(1024)
            print(resp.decode())
                 
            if not resp:
                print("not data_received")
                break

        dataSocket.close()
        resp = clientSocket.recv(1024)
        print(resp.decode())

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

    elif (command == "get"):
        data_port = random.randint(1025, 65535)  # Choose a random port number
        open_con = f"127,0,0,1,{data_port // 256},{data_port % 256}"
        print(type(data_port))

        clientSocket.send(f"PORT {open_con}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode())

        clientSocket.send("RETR redta.txt\r\n".encode())
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
