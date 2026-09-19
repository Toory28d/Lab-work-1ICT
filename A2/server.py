import socket
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
    """Parse one command line and return the text reply (no trailing newline)."""
    if not line:
        return None  # client disconnected or sent nothing

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


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f'[SERVER] Listening on {HOST}:{PORT}')

        conn, addr = server_sock.accept()
        with conn:
            print(f'[SERVER] Connected by {addr}')
            while True:
                line = recv_line(conn)
                if not line:
                    print('[SERVER] Client disconnected')
                    break

                print(f'[SERVER] Received: {line}')
                reply = process_command(line)
                conn.sendall((reply + '\n').encode('utf-8'))

                if line.upper() == 'QUIT':
                    print('[SERVER] Client sent QUIT, closing connection')
                    break


if __name__ == '__main__':
    main()
