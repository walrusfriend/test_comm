import socket
import threading
import queue

clients = {}  # addr -> (username, queue.Queue())

def handle_client(sock, addr):
    username, q = clients[addr]
    print(f"Started chat handler for {addr} ({username})")
    sock.sendto(f"Welcome to UDP chat, {username}!".encode(), addr)
    while True:
        try:
            data = q.get()
            if data is None:
                break
            print(f"Received from {username}@{addr}: {data}")
            # Broadcast the received message to all other clients
            for client_addr, (other_username, _) in clients.items():
                if client_addr != addr:
                    msg = f"{username}: {data.decode()}"
                    sock.sendto(msg.encode(), client_addr)
        except Exception as e:
            print(f"Handler error for {addr}: {e}")
            break

def udp_chat_server(listen_ip: str = "127.0.0.1", listen_port: int = 10000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    print(f"UDP chat server listening on {listen_ip}:{listen_port}")
    try:
        while True:
            data, addr = sock.recvfrom(4096)
            if addr not in clients:
                msg = data.decode().strip()
                if msg.lower().startswith("connect "):
                    username = msg[8:].strip()
                    if not username:
                        sock.sendto(b"Username required. Usage: connect username", addr)
                        continue
                    clients[addr] = (username, queue.Queue())
                    threading.Thread(target=handle_client, args=(sock, addr), daemon=True).start()
                    print(f"Client {addr} connected as '{username}'.")
                else:
                    sock.sendto(b"Send 'connect username' to join the chat.", addr)
                    continue
            if addr in clients:
                clients[addr][1].put(data)
    except Exception as e:
        print(f"UDP chat server error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_chat_server()
