import socket
from urllib.parse import urlparse


def get_ip_addresses(url):
    # Use urlparse to extract the domain from the URL
    domain = urlparse(url).netloc

    try:
        # Use socket to get the IP addresses associated with the domain
        ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses[2]
    except socket.gaierror:
        print("Error: Unable to resolve the IP address for the given URL.")
        return []


def scan_ports(ip_address, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


def main():
    # Get the target URL from the user
    target_url = input("Enter the target URL: ")

    # Get the IP addresses associated with the domain
    ip_addresses = get_ip_addresses(target_url)

    if not ip_addresses:
        return

    print("\nIP Addresses:")
    for ip_address in ip_addresses:
        print(ip_address)

    # Define a list of common ports to scan
    popular_ports = [21, 22, 23, 25, 53, 80, 110, 119, 123, 143,
                     161, 194, 443, 465, 587, 993, 995, 1433, 1521,
                     3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017,
                     27018, 27019, 5000]

    # Scan each IP address for open ports
    print("Now searching for ports. May take a little time")
    for ip_address in ip_addresses:
        open_ports = scan_ports(ip_address, popular_ports)

        print(f"\nOpen ports for {ip_address}:")
        if open_ports:
            for port in open_ports:
                print(f"Port {port} is open")
        else:
            print("No open ports found")


if __name__ == "__main__":
    main()
