import socket
import threading
import queue

clients = {}

def handle_client(sock, addr):
    print(f"Started handler for {addr}")
    sock.sendto(b'Connection established', addr)
    while True:
        try:
            data = clients[addr].get()
            if data is None:
                break
            print(f"Received from {addr}: {data}")
            # Broadcast the received message to all other clients
            for client_addr, q in clients.items():
                if client_addr != addr:
                    sock.sendto(data, client_addr)
        except Exception as e:
            print(f"Handler error for {addr}: {e}")
            break

def udp_server(listen_ip: str = "127.0.0.1", listen_port: int = 9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    print(f"UDP chat server listening on {listen_ip}:{listen_port}")
    try:
        while True:
            data, addr = sock.recvfrom(4096)
            if addr not in clients:
                clients[addr] = queue.Queue()
                threading.Thread(target=handle_client, args=(sock, addr), daemon=True).start()
            clients[addr].put(data)
    except Exception as e:
        print(f"UDP server error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_server()