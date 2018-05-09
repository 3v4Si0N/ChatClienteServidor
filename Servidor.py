from socket import *
from threading import Thread as Process

class Servidor():
        def __init__(self): # Inicializamos puerto, host, lista clients y esperamos a que se conecte alguien al server
                self.port = 9999
                self.host = "192.168.1.175"
                self.clients = []
                self.escuchar()

        def escuchar(self):
                try:
                        sock = socket(AF_INET, SOCK_STREAM) # Creamos un socket
                        sock.bind((self.host, self.port)) # Conectamos el socket al puerto y host
                        sock.listen(5) # Escuchamos a 5 maximo
                        print("Server is running on "+ str(self.port))
                        print("Waiting for clients....")
                        trds = []
                        for i in range(5):
                                conn, addr = sock.accept() # Aceptamos la conexion
                                self.clients.append(conn) # Insertamos el objeto del socket en la lista clients
                                t = Process(target=self.clientHandler, args = (conn, addr)) # Creamos un thread por cada cliente que se conecta
                                trds.append(t) # Insertamos el thread en la lista trds
                                t.start() # Iniciamos el thread
                        for t in trds:
                                t.join() # Aceptamos el thread
                except KeyboardInterrupt:
                        print ("Exiting..")
                        sock.close() # Si ocurre alguna excepcion cerramos el socket
                        return

        def clientHandler(self, conn, addr):
            print(addr, "has been connected")
            print(self.clients)
            try:
                while True:
                        data = conn.recv(1024)
                        if not len(data): # Si no hay nada que recibir salimos del bucle infinito
                                break
                        else:
                                for i in self.clients:
                                        if i != conn: # Enviamos datos a todos los clientes menos a nosotros mismos
                                                i.send(data)                            
            except:
                direction = "%s:%i" %addr
                print(direction + " has been disconnected")
                self.clients.remove(conn) # Si alguien se desconecta eliminamos el objeto conn de la lista clients
                conn.close() # Cerramos la conexion
                return

Servidor()
