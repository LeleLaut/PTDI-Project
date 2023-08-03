import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable UDP broadcast
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set the broadcast address and port
broadcast_address = '192.168.168.255'  # Use the broadcast address of your local network
port = 50000 # Choose a port number

# Data to be broadcasted (replace this with your actual data)
while True:
    data_to_broadcast = "Hello, clients!"

    # Broadcast the data
    server_socket.sendto(data_to_broadcast.encode('utf-8'), (broadcast_address, port))

    print(data_to_broadcast)
# Close the socket
server_socket.close()
