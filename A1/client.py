import socket

HOST = '127.0.0.1'
PORT = 5050


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((HOST, PORT))
        message = input('Enter a message to send: ')
        client_sock.sendall(message.encode('utf-8'))
        reply = client_sock.recv(1024)
        print(f'[CLIENT] Server replied: {reply.decode("utf-8")}')


if __name__ == '__main__':
    main()
