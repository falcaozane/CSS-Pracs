
import socket

def server_program():
    host = socket.gethostname()
    port = 5003
    server_socket = socket.socket()
    server_socket.bind((host, port)) 
    server_socket.listen(1)
    conn, address = server_socket.accept() 
    print("Connection from: " + str(address))
    
   
    data = conn.recv(1024).decode().split(',')
    n, g, a = int(data[0]), int(data[1]), int(data[2])
    
    y = int(input("Enter y -> "))
    print("The public key of alice is", a)
   
    b = (g ** y) % n
    conn.send(str(b).encode())
    
  
    k1 = (a ** y) % n
    print('The Symmetric key is:', k1)
    
    conn.close()

if __name__ == '__main__':
    server_program()



