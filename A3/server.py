import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5050


def recv_line(conn):
    buffer = b''
    while not buffer.endswith(b'\n'):
        chunk = conn.recv(1)
        if not chunk:
            break
        buffer += chunk
    return buffer.decode('utf-8').strip()


def process_command(line):
    parts = line.split(' ', 1)
    cmd = parts[0].upper()

    if cmd == 'ECHO':
        text = parts[1] if len(parts) > 1 else ''
        return text
    elif cmd == 'TIME':
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif cmd == 'QUIT':
        return 'BYE'
    else:
        return 'ERROR: unknown command'


def handle_client(conn, addr):
    with conn:
        print(f'[SERVER] Connected by {addr}')
        while True:
            line = recv_line(conn)
            if not line:
                print(f'[SERVER] {addr} disconnected')
                break

            print(f'[SERVER] {addr} sent: {line}')
            reply = process_command(line)
            conn.sendall((reply + '\n').encode('utf-8'))

            if line.upper() == 'QUIT':
                print(f'[SERVER] {addr} sent QUIT, closing connection')
                break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f'[SERVER] Listening on {HOST}:{PORT}')

        while True:
            conn, addr = server_sock.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == '__main__':
    main()
