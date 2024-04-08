import socket
import sys
from datetime import datetime

def resolve_ip(target_host):
    try:
        target_ip = socket.gethostbyname(target_host)
        return target_ip
    except socket.gaierror:
        print(f"Cannot resolve '{target_host}': Unknown host")
        sys.exit(1)

def scan_ports(target_ip, ports_to_scan):
    # Create an empty list to store open ports
    open_ports = []

    # Start the scan
    start_time = datetime.now()
    print(f"Starting port scan for {target_ip} at {start_time}")

    # Scan the ports
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # Set a timeout of 100 milliseconds
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    # Print the open ports
    end_time = datetime.now()
    print(f"Port scan completed in {end_time - start_time}")
    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port in open_ports:
            print(port)
    else:
        print(f"No open ports found on {target_ip}")

if __name__ == "__main__":
    # Prompt the user to enter the target domain name
    target_host = input("Enter the target domain name (e.g., www.google.com): ")

    # Resolve the domain name to an IP address
    target_ip = resolve_ip(target_host)

    # Define the range of ports to scan
    ports_to_scan = list(range(1, 1001))

    # Call the scan_ports function with the resolved IP address
    scan_ports(target_ip, ports_to_scan)
