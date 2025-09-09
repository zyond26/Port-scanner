

import socket   #socket là thư viện mạng trong python -> cho phép tạo kết nối TCP/UDP, gửi và nhận dữ liệu
import argparse # dùng để xử lý argument trên dòng lệnh 
import threading # cho phép chạy đa luồng -> quét nhiều port song song -> faster hihi

# -------------------------
# Hàm quét TCP port
# -------------------------
def tcp_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.AF_INET dùng IPv4
        # socket.SOCK_STREAM: dùng TCP kết nối hướng luồng dữ liệu tin cậy
        sock.settimeout(1)  # tránh treo khi không phản hồi
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                # Banner grabbing
                sock.send(b'Hello\r\n')
                banner = sock.recv(1024).decode().strip()
                print(f"[+] TCP {port} OPEN - Banner: {banner}")
            except:
                print(f"[+] TCP {port} OPEN")
        sock.close()
    except Exception as e:
        pass

# -------------------------
# Hàm quét UDP port
# -------------------------
def udp_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b"Hello", (target, port))
        data, _ = sock.recvfrom(1024)
        print(f"[+] UDP {port} OPEN - Response: {data}")
    except socket.timeout:
        print(f"[?] UDP {port} No response (maybe open|filtered)")
    except:
        pass
    finally:
        sock.close()

# -------------------------
# Main function
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP/hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range, e.g. 20-100")
    parser.add_argument("-u", "--udp", action="store_true", help="Enable UDP scan")
    args = parser.parse_args()

    target = args.target
    start_port, end_port = map(int, args.ports.split("-"))

    print(f"[*] Scanning {target} ports {start_port}-{end_port}...")
    threads = []

    for port in range(start_port, end_port + 1):
        if args.udp:
            t = threading.Thread(target=udp_scan, args=(target, port))
        else:
            t = threading.Thread(target=tcp_scan, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
