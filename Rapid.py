import socket
import sys
from datetime import datetime

def scan_ports(target_host, ports_to_scan):
    # Create an empty list to store open ports
    open_ports = []

    # Start the scan
    start_time = datetime.now()
    print(f"Starting port scan for {target_host} at {start_time}")

    # Resolve the hostname to an IP address
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(f"Cannot resolve '{target_host}': Unknown host")
        return []

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
        print(f"Open ports on {target_host}:")
        for port in open_ports:
            print(port)
    else:
        print(f"No open ports found on {target_host}")

    return open_ports

if __name__ == "__main__":
    # Prompt the user to enter the target IP address
    target_host = input("Enter the target IP address: ")

    # Define the range of ports to scan
    ports_to_scan = list(range(1, 1001))

    # Call the scan_ports function with user-defined target IP address
    open_ports = scan_ports(target_host, ports_to_scan)
