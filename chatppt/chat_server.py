import socket
import os

def ftp_server(port, directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print("FTP Server started on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection established from", client_address)

        try:
            while True:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                if request.startswith("GET"):
                    filename = request.split()[1]
                    file_path = os.path.join(directory, filename)
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            data = file.read()
                        client_socket.sendall(data)
                    else:
                        client_socket.sendall(b"File not found")
                elif request == "QUIT":
                    client_socket.sendall(b"Goodbye!")
                    break
                else:
                    client_socket.sendall(b"Invalid command")
        except Exception as e:
            print("Error:", e)
        finally:
            client_socket.close()

if __name__ == "__main__":
    ftp_server(10000, "./ftp_directory")
