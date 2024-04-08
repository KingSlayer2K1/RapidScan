import socket
import sys
from datetime import datetime
import requests

def resolve_ip(target_host):
    try:
        target_ip = socket.gethostbyname(target_host)
        return target_ip
    except socket.gaierror:
        print(f"Cannot resolve '{target_host}': Unknown host")
        sys.exit(1)

def scan_ports(target_ip, ports_to_scan):
    # Create an empty list to store open ports and available HTTP services
    open_ports = []
    http_services = []

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
            # Check if the port corresponds to an HTTP service (port 80 or 443)
            if port in [80, 443]:
                http_services.append(port)
        sock.close()

    # Check if HTTP services are available
    for port in http_services:
        if port == 80:
            url = f"http://{target_ip}"
        elif port == 443:
            url = f"https://{target_ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"HTTP service is available at {url}")
        except requests.ConnectionError:
            pass

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
    target_host = input("Enter the target domain name or IP address: ")

    # Resolve the domain name to an IP address
    target_ip = resolve_ip(target_host)

    # Define the range of ports to scan
    ports_to_scan = list(range(1, 1001))

    # Call the scan_ports function with the resolved IP address
    scan_ports(target_ip, ports_to_scan)
