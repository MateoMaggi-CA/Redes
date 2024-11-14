import socket
import threading

ENCODING = 'utf-8'
BUFFER_SIZE = 2048

class Cliente:

    #Inicializa el objeto Cliente
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.BUFFER = BUFFER_SIZE
        self.nombre = input("Escribi tu Nombre: ")
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
        self.conectado = False
        self.ConeAlServer()

    #Método para establecer la conexión con el servidor
    def ConeAlServer(self):
        try:
            self.cliente.connect((self.host, self.port))
            self.conectado = True
            print("CLIENTE: Conectado al servidor.")
            self.inicioThreading()
        except socket.error as e:
            print(f"CLIENTE: Error al conectar al servidor: {e}")
            exit()

    #Método para iniciar hilos que manejan la recepción y envío de mensajes
    def inicioThreading(self):
        hilo_recepcion = threading.Thread(target=self.receptor)
        hilo_emision = threading.Thread(target=self.emisor)
        hilo_recepcion.start()
        hilo_emision.start()

    #Método para enviar mensajes
    def emisor(self):
        while True:
            texto = input('')  # Espera la entrada del usuario para enviar un mensaje

        #Si el mensaje es un comando para cambiar de estado
            if texto.startswith("/estado"):
                partes = texto.split()
                if len(partes) > 1:
                # Envía el comando de estado al servidor solo si el estado está especificado
                    self.cliente.send(texto.encode(ENCODING))
                    print(f"CLIENTE: Cambiaste tu estado a '{partes[1]}'")  # Muestra el nuevo estado en el cliente
                else:
                    print("CLIENTE: Debes especificar un estado. Usa '/estado <estado>'.")
            elif texto == "/listar":
                self.cliente.send(texto.encode(ENCODING))  # Envía el comando al servidor
            elif texto == "/desconectar":
                self.cliente.send(texto.encode(ENCODING))  # Envía el comando de desconexión al servidor
                print("CLIENTE: Desconectando a todos los usuarios.")
                break
            elif texto == "/perfil":
                self.cliente.send(texto.encode(ENCODING))  # Envía el comando de perfil al servidor
            elif texto == "/salir":
                self.cliente.send(texto.encode(ENCODING))  # Envía el comando de salida
                print("CLIENTE: Desconectándote del servidor.")
                break
            elif texto.startswith("!"):
                self.cliente.send(texto.encode(ENCODING))  # Envía el mensaje tal cual al servidor
            else:
                Textoalternativo = f"{self.nombre}: {texto}"  # Formatea el mensaje con el apodo
                self.cliente.send(Textoalternativo.encode(ENCODING))  # Envía el mensaje formateado al servidor


    #Método para recibir mensajes del servidor
    def receptor(self):
        while self.conectado:
            try:
                texto = self.cliente.recv(self.BUFFER)
                if not texto:
                    print("CLIENTE: Conexión cerrada por el servidor.")
                    self.conectado = False
                    self.cliente.close()
                    break
                if texto == b"@nickname":
                    self.cliente.send(self.nombre.encode(ENCODING))
                else:
                    print(f"{texto.decode(ENCODING)}")
            except Exception as e:
                print(f"CLIENTE: Ocurrió un error en la conexión: {e}")
                self.conectado = False
                self.cliente.close()
                break

#Punto de entrada del programa
if __name__ == "__main__":
    cliente = Cliente()
