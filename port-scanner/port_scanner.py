import socket
import threading
from datetime import datetime

TARGET = "192.168.56.102"
PORTS = range(1, 1025)
TIMEOUT = 1
THREADS = 100
OUTPUT = "scan_report.txt"

open_ports = []
lock = threading.Lock()

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(TIMEOUT)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner[:80] if banner else "No banner"
    except:
        return "No banner"

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            banner = grab_banner(ip, port)
            with lock:
                open_ports.append((port, banner))
                print(f"[OPEN] Port {port} | {banner}")
    except:
        pass

def run_scan():
    print(f"Scanning {TARGET}...")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    threads = []
    for port in PORTS:
        t = threading.Thread(target=scan_port, args=(TARGET, port))
        threads.append(t)
        t.start()
        if len(threads) >= THREADS:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

    open_ports.sort()
    with open(OUTPUT, "w") as f:
        f.write(f"Scan results for {TARGET}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if open_ports:
            for port, banner in open_ports:
                f.write(f"Port {port} OPEN | {banner}\n")
        else:
            f.write("No open ports found.\n")

    print(f"\n{len(open_ports)} open ports found.")
    print(f"Results saved to {OUTPUT}")

if __name__ == "__main__":
    run_scan()
