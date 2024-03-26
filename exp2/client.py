import socket

def client_program():
    host = socket.gethostname()
    port = 5003
    client_socket = socket.socket() 
    client_socket.connect((host, port)) 
    n = int(input(" Enter n -> "))
    g = int(input(" Enter g -> ")) 
    x = int(input("enter x->"))
    

    a = (g ** x) % n
    client_socket.send(f"{n},{g},{a}".encode()) 
    b = int(client_socket.recv(1024).decode())
    print("The public key of bob is ", b )
    
  
    k1 = (b ** x) % n
    print('The Symmetric key is:', k1)
    
    client_socket.close()

if __name__ == '__main__':
    client_program()


