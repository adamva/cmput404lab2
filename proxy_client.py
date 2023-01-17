#!/usr/bin/env python3
import socket, sys

PRX_HST = 'localhost'
PRX_PRT = 8002
BUFFER_SIZE = 4096

# Create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    # print('Socket created successfully')
    return s

# Get IP for hostname
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    # print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# Send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
        serversocket.shutdown(socket.SHUT_WR)
    except socket.error:
        print ('Send failed')
        sys.exit()
    # print("Payload sent successfully")

def main():
    try:        
        req_data = b'GET / HTTP/1.0\nHost: www.google.com\n\n'

        # Create client socket and connect to proxy
        s = create_tcp_socket()
        prx_ip = get_remote_ip(PRX_HST)
        s.connect((prx_ip , PRX_PRT))
        print (f'Connected to {PRX_HST} on {prx_ip}:{PRX_PRT}')

        # Send the data and shutdown
        send_data(s, req_data)
        s.shutdown(socket.SHUT_WR)

        # Read response
        full_data = b""
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                 break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        s.close()

if __name__ == "__main__":
    main()

