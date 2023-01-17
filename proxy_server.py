#!/usr/bin/env python3
import socket, time
from threading import Thread

# Define server binding
BND_HST = "localhost"
BND_PRT = 8002
# Define proxy target
TGT_HST = 'www.google.com'
TGT_PRT = 80
BUFFER_SIZE = 4096

def create_tcp_socket():
    # print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
    # print('Socket created successfully')
    return s

# Get IP for hostname
def get_remote_ip(host):
    # print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print (f'Hostname {host} could not be resolved')
    # print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# Send HTTP request
def send_request(host, port, req_data):
    rsp_data = b''
    try:
        # Create client socket & send request
        s = create_tcp_socket()
        host_ip = get_remote_ip(host)
        s.connect((host_ip, port))
        s.send(req_data)
        s.shutdown(socket.SHUT_WR)

        # Read response
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            rsp_data += data
    except socket.error:
        print(f'Failed to send request to {host}:{port}')
    finally:
        s.close()
    return rsp_data

# Proxy requests and responses for incoming connections
def handle_connection(conn, addr):
    try:
        req_data = b''
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            req_data += data
        rsp_data = send_request(TGT_HST, TGT_PRT, req_data)
        conn.send(rsp_data)
        conn.shutdown(socket.SHUT_WR)
    except socket.error:
        print(f'Failed to proxy request for {addr} E: {socket.error}')
    finally:
        conn.close()

def main():
    # Create server socket & listen for incoming connections
    print(f'Starting proxy server on {BND_HST}:{BND_PRT}')
    svr_conn = create_tcp_socket()
    svr_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    svr_conn.bind((BND_HST, BND_PRT))
    svr_conn.listen(2)

    # Accept incoming requests
    while True:
        req_conn, req_addr = svr_conn.accept()
        print(f"Connected by {req_addr}")
        thread = Thread(target=handle_connection, args=(req_conn, req_addr))
        thread.run()
    
    svr_conn.close()

if __name__ == "__main__":
    main()
