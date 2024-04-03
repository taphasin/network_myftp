import socket

def ftp_client(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    print("Connected to FTP Server")

    try:
        while True:
            command = input("Enter command (GET <filename>, QUIT): ").strip()
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            print(response)
            if response == "Goodbye!" or not response:
                break
            elif response == "File not found":
                continue
            # elif command.startswith("GET"):
            #     data = client_socket.recv(4096)
            #     with open(command.split()[1], "wb") as file:
            #         file.write(data)
            #     print("File downloaded successfully")
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    ftp_client("localhost", 10000)
