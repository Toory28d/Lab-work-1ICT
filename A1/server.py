import socket

HOST = '127.0.0.1'
PORT = 5050


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f'[SERVER] Listening on {HOST}:{PORT}')

        conn, addr = server_sock.accept()
        with conn:
            print(f'[SERVER] Connected by {addr}')
            data = conn.recv(1024)
            message = data.decode('utf-8')
            print(f'[SERVER] Received: {message}')
            conn.sendall(data)  # echo back


if __name__ == '__main__':
    main()
