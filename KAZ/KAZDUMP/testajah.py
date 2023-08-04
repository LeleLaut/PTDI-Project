import socket

def get_local_wifi_ipv4_address():
    try:
        # Create a socket object using the AF_INET (IPv4) and SOCK_DGRAM (UDP) parameters
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a public IP address (e.g., Google's DNS server) to get the local IP
        s.connect(("8.8.8.8", 80))
        # Get the local IP address
        local_ip = s.getsockname()[0]
        ip_components = local_ip.split('.')
        # Change the last three digits to '255'
        modified_ip = '.'.join(ip_components[:-1] + ['255'])
        return modified_ip
    except socket.error as e:
        print(f"Error occurred while retrieving the local IP address: {e}")
        return None

if __name__ == "__main__":
    wifi_ipv4_address = get_local_wifi_ipv4_address()
    if wifi_ipv4_address:
        print(f"Local Wi-Fi IPv4 Address: {wifi_ipv4_address}")
    else:
        print("Could not retrieve the local Wi-Fi IPv4 address.")
