import socket
import threading
import queue
import logging
from datetime import datetime

log_filename = f"scan_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"[OPEN]   Port {port} \n")
            logging.info(f"OPEN Port {port}")
        elif result == 11:  # timeout
            print(f"[TIMEOUT] Port {port}")
            logging.info(f"TIMEOUT Port {port}")
        else:
            print(f"[CLOSED] Port {port}\n")
            logging.info(f"CLOSED Port {port}")

        s.close()
    except Exception as e:
        print(f"[ERROR] Port {port}: {e}")
        logging.error(f"ERROR Port {port}: {e}")


def worker(ip, q):
    while not q.empty():
        port = q.get()
        scan_port(ip, port)
        q.task_done()


def start_scan(ip, start_port, end_port, threads_count=50):
    print(f"\nStarting scan on {ip}...")
    print(f"Port Range: {start_port}-{end_port}")
    print(f"Logs saved to: {log_filename}\n")

    q = queue.Queue()

    for port in range(start_port, end_port + 1):
        q.put(port)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=worker, args=(ip, q))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

   
    q.join()

    print("\nScan Completed!")
    logging.info("Scan Completed")


if __name__ == "__main__":
    print("=== TCP PORT SCANNER (Multithreaded) ===")

    ip = input("Enter target IP/Host: ")

    print("\n1. Scan single port")
    print("2. Scan range of ports")

    choice = input("Choose option (1/2): ")

    if choice == "1":
        port = int(input("Enter port number: "))
        start_scan(ip, port, port)

    elif choice == "2":
        start_p = int(input("Start port: "))
        end_p = int(input("End port: "))
        start_scan(ip, start_p, end_p)

    else:
        print("Invalid choice!")

