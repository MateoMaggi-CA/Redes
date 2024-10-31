#Realizar un programa cliente-servidor concurrente (thread) donde cada cliente va a tener un id y un nickname/apodo que debe ser solicitado
#al momento de conectarse y agregado a una tabla de usuarios en mysql junto con un id, fecha de ultima conexión y fecha de creación 
#siendo ambos datetime o timestamp

id int, nickname varchar 50,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated/connected_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#El servidor debe permitir a los clientes comunicarse entre si, teniendo la posibilidad de mandar comandos 
#Si envía un mensaje ese mensaje lo reciben todos ej: Hola gente ---> lo deben recibir todos
#Si envía como primer caracter un # usuario + mensaje ej: #Juan como andas juan? y ese mensaje solo debe ir a juan verificando si existe
#Si envía como primer caracter / corresponde a un comando
Ej: /listar y ese comando debe mostrar todos los usuarios que estaban conectados
Ej: /desconectar y ese comando debe desconectar a todos los usuarios
Ej: /salir y ese comando debe cerra la conexión

import socket
import threading


connections = []
connectionCount = 0 

class Cliente(threading.Thread):

    def init(self, socket,address,id):
        threading.Thread.init(self)
        self.socket = socket
        self.address = address
        self.id = id

    def str(self):
        return str(self.id + " " + str(self.address))

    def run(self):
        while True:
            try:
                msg = self.socket.recv(1024)
                print(msg.decode())
            except:
                print("El cliente " + str(self.address) + " se desconectó ")
                self.socket.close()
                connections.remove(self.socket)
                break
            if msg != "":
                print(str(msg.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.sendall(msg)



def clientHandle(socket):

    while True:
        global connectionCount
        conn, addr = socket.accept()
        connections.append(Cliente(conn, addr, connectionCount))
        connections[connectionCount].start() #startea
        connectionCount += 1

def main():

    host= '127.0.0.1'
    port= 5000

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host,port))
    server_sock.listen(10) #cantidad de usuarios en cola de espera

    nconnthread = threading.Thread(target= clientHandle , args=(server_sock,))
    nconnthread.start()

main()