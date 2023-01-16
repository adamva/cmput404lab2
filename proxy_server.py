#!/usr/bin/env python3
import socket
import time

#define address & buffer size
HOST = ""
PORT = 8002
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            # print('conn object', conn)
            print("Connected by", addr)
            
            # get data from client 
            full_data = conn.recv(BUFFER_SIZE)
            
            # create socket & connect to google
            g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            g_ip = socket.gethostbyname('www.google.com')
            g_sock.connect((g_ip , 80))
            
            # pass along data from client to google
            g_sock.sendall(full_data) # .encode()
            g_sock.shutdown(socket.SHUT_WR)
            
            # read back what google says
            g_data = b""
            while True:
                data = g_sock.recv(4096)
                if not data:
                    break
                g_data += data

            # send what google said back to client
            conn.sendall(g_data)        
            
            g_sock.close()
            conn.close()

if __name__ == "__main__":
    main()
