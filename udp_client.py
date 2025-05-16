import socket
import threading

def create_udp_connection(server_ip: str, server_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))  # Bind to an ephemeral port to receive messages
    return sock, (server_ip, server_port)

def handle_udp_requests(listen_ip: str, listen_port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    print(f"Listening for UDP packets on {listen_ip}:{listen_port}...")
    try:
        while True:
            data, addr = sock.recvfrom(4096)
            print(f"Received from {addr}: {data}")
            # Echo back the received data
            sock.sendto(data, addr)
    except KeyboardInterrupt:
        print("UDP handler stopped.")
    finally:
        sock.close()

def receive_messages(sock):
    while True:
        try:
            data, server = sock.recvfrom(4096)
            print(f"{data.decode()}")
        except Exception:
            break

if __name__ == "__main__":
    server_ip = "45.132.19.1"
    server_port = 10000  # Must match the port in main.py
    sock, addr = create_udp_connection(server_ip, server_port)
    try:
        # Send connect message first for chat
        username = input("Enter your username: ")
        sock.sendto(f"connect {username}".encode(), addr)
        recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
        recv_thread.start()
        while True:
            line = input()
            if line.lower() == "exit":
                break
            sock.sendto(line.encode(), addr)
    finally:
        sock.close()

# Example usage:
# sock, addr = create_udp_connection("127.0.0.1", 9999)
# sock.sendto(b"Hello, UDP!", addr)
# data, server = sock.recvfrom(4096)
# print("Received:", data)
# sock.close()
