import socket
import threading
import pymysql
from datetime import datetime

#Configuración de codificación y tamaño del buffer
ENCODING = 'utf-8'
BUFFER_SIZE = 2048

class Servidor:
    def __init__(self, host="127.0.0.1", port=5000):
        """
        Constructor para la clase Servidor.
        Establece los atributos y configura el socket para el servidor.
        """
        self.host = host  
        self.port = port  
        self.buffer_size = BUFFER_SIZE  
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Inicializa un socket TCP/IP
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Permite reutilizar la IP y puerto
        self.servidor.bind((self.host, self.port))  #Asocia el socket con la IP y puerto definidos
        self.servidor.listen() 
        self.clientes = []  
        self.nicknames = []  
        self.hilos = []  
        self.running = True
        self.estados = []  

        print(f"SERVIDOR: Iniciado en {self.host}:{self.port}.")  #Notificación de inicio del servidor

        #Establece la conexión a la base de datos MySQL
        try:
            self.db = pymysql.connect(
                host="127.0.0.1",  #IP de la base de datos
                user="root",       #Usuario de la base de datos
                password="",       #Contraseña del usuario
                database="Redes"   #Nombre de la base de datos
            )
            self.cursor = self.db.cursor()  #Crea un cursor para ejecutar SQL
            print("SERVIDOR: Conexión exitosa con la base de datos.")  #Mensaje de éxito de conexión
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")  #Mensaje en caso de error de conexión
            self.running = False  #Detiene el servidor si falla la conexión a la base de datos

    def transmitir_mensaje(self, mensaje, remitente):
        """
        Envía un mensaje a todos los clientes conectados, excepto al que lo envía.
        Si el mensaje es privado (empieza con '!'), lo envía solo al destinatario.
        """
        mensaje_decodificado = mensaje.decode(ENCODING)  #Convierte el mensaje de bytes a texto

        
        if mensaje_decodificado.startswith("!"):
            partes = mensaje_decodificado.split()  
            nombre_destino = partes[0][1:]  

            
            if nombre_destino in self.nicknames:
                indice_destino = self.nicknames.index(nombre_destino)  
                cliente_destino = self.clientes[indice_destino]  

                indice_remitente = self.clientes.index(remitente)  
                nombre_remitente = self.nicknames[indice_remitente]  

                #Crea el mensaje de chat privado
                mensaje_privado = f"{nombre_remitente} (Privado): {' '.join(partes[1:])}"
                #Envía el mensaje privado solo al destinatario
                cliente_destino.send(mensaje_privado.encode(ENCODING))
                return 
            else:
                #Informa al remitente si el destinatario no existe
                remitente.send(f"[SERVIDOR]: El usuario '{nombre_destino}' no existe.".encode(ENCODING))
                return 
        else:
            #Envía el mensaje a todos excepto al remitente
            for cliente in self.clientes:
                if cliente != remitente:
                    try:
                        cliente.send(mensaje)  #Envía el mensaje a cada cliente
                    except Exception as e:
                        print(f"Error al enviar mensaje a un cliente: {e}")  #Mensaje de error si falla el envío
                        self.desconectar_cliente(cliente)  #Desconecta al cliente si hay un problema

    """def manejar_mensaje(self, cliente):
        """
        
    """
        while self.running:
            try:
                mensaje = cliente.recv(self.buffer_size)  #Recibe el mensaje del cliente
                if not mensaje:
                    #Si no llega mensaje, el cliente se ha desconectado
                    self.desconectar_cliente(cliente)
                    break

                mensaje_decodificado = mensaje.decode(ENCODING)  #Decodifica el mensaje

               
                if mensaje_decodificado == "/listar":
                    self.listar_usuarios_conectados(cliente)  #Envía la lista de usuarios conectados
                elif mensaje_decodificado == "/desconectar":
                    self.desconectar_clientes()  #Desconecta a todos los usuarios
                    break
                elif mensaje_decodificado == "/perfil":
                    self.obtener_perfil(cliente)  #Envía el perfil del usuario
                elif mensaje_decodificado == "/salir":
                    self.desconectar_cliente(cliente)  #Desconecta al cliente
                    break
                else:
                   
                    self.transmitir_mensaje(mensaje, cliente)
            except Exception as e:
                print(f"Ocurrió un error con un cliente: {e}")  #Mensaje de error si ocurre un problema
                self.desconectar_cliente(cliente)  #Desconecta al cliente si hay un error
                break"""
    
    def listar_usuarios_conectados(self, cliente):
        lista_usuarios = "[SERVIDOR] - Usuarios Conectados:\n" + "\n".join(
            f"{nickname} - {estado}" for nickname, estado in zip(self.nicknames, self.estados)
    )
        print(f"DEBUG: Enviando lista de usuarios: \n{lista_usuarios}")
        try:
            cliente.send(lista_usuarios.encode(ENCODING))
        except Exception as e:
            print(f"Error al enviar la lista de usuarios: {e}")
            self.desconectar_cliente(cliente)

    def manejar_mensaje(self, cliente):
        while self.running:
            try:
                mensaje = cliente.recv(self.buffer_size)
                if not mensaje:
                    self.desconectar_cliente(cliente)
                    break

                mensaje_decodificado = mensaje.decode(ENCODING)

                if mensaje_decodificado.startswith("/estado"):
                    partes = mensaje_decodificado.split()
                
                    if len(partes) > 1:
                        nuevo_estado = partes[1]
                        indice = self.clientes.index(cliente)
                        self.estados[indice] = nuevo_estado  # Actualiza el estado del cliente
                        cliente.send(f"[SERVIDOR]: Estado cambiado a '{nuevo_estado}'.".encode(ENCODING))
                        print(f"DEBUG: Estado de {self.nicknames[indice]} cambiado a '{nuevo_estado}'.")
                    else:
                        cliente.send("[SERVIDOR]: Comando de estado incorrecto. Usa '/estado <estado>'.".encode(ENCODING))
                elif mensaje_decodificado == "/listar":
                    self.listar_usuarios_conectados(cliente)
                elif mensaje_decodificado == "/desconectar":
                    self.desconectar_clientes()
                    break
                elif mensaje_decodificado == "/perfil":
                    self.obtener_perfil(cliente)
                elif mensaje_decodificado == "/salir":
                    self.desconectar_cliente(cliente)
                    break
                else:
                    self.transmitir_mensaje(mensaje, cliente)
            except Exception as e:
                print(f"Ocurrió un error con un cliente: {e}")
                self.desconectar_cliente(cliente)
                break


    """def listar_usuarios_conectados(self, cliente):
        """
        #Envía al cliente que lo pide una lista de los usuarios conectados.
    """
        lista_usuarios = "[SERVIDOR] - Usuarios Conectados:\n" + "\n".join(self.nicknames)
        try:
            cliente.send(lista_usuarios.encode(ENCODING))  #Envía la lista al cliente
        except Exception as e:
            print(f"Error al enviar la lista de usuarios: {e}")  #Mensaje de error si falla el envío
            self.desconectar_cliente(cliente)  #Desconecta al cliente si hay un problema"""

   
    

    def desconectar_clientes(self):
        """
        Desconecta a todos los clientes que están conectados al servidor.
        """
        for cliente in self.clientes[:]:  #Recorre una copia de la lista de clientes
            try:
                cliente.send("Desconectando a todos los usuarios...".encode(ENCODING))  #Informa al cliente
            except Exception as e:
                print(f"Error al enviar mensaje de desconexión: {e}")  #Mensaje de error si falla el envío
            self.desconectar_cliente(cliente)  e
        self.clientes.clear()  
        self.nicknames.clear()  

    def obtener_perfil(self, cliente):
        """
        Recupera y envía al cliente su perfil desde la base de datos.
        """
        indice = self.clientes.index(cliente)  #Encuentra la posición del cliente
        nickname = self.nicknames[indice]  #Obtiene el apodo del cliente

        try:
            #Realiza una consulta SQL para obtener la información del usuario
            with self.db.cursor() as cursor:
                cursor.execute("SELECT id, created_at, connected_at FROM usuarios WHERE nickname = %s", (nickname,))
                perfil = cursor.fetchone()  #Obtiene el primer resultado de la consulta

            if perfil:
                id_usuario, created_at, connected_at = perfil  #Descompone los datos obtenidos
                #Crea el mensaje con los datos del perfil
                mensaje_perfil = f" - ID: {id_usuario}\n - Fecha de Creación: {created_at}\n - Última Conexión: {connected_at}"
                cliente.send(mensaje_perfil.encode(ENCODING))  #Envía los datos del perfil al cliente
            else:
                #Informa al cliente si el perfil no fue encontrado
                cliente.send("[SERVIDOR]: No se encontró el perfil.".encode(ENCODING))
        except Exception as e:
            print(f"Error al obtener el perfil del usuario: {e}")  #Mensaje de error si ocurre un problema
            self.desconectar_cliente(cliente)  

    def desconectar_cliente(self, cliente):
        """
        Desconecta a un cliente en particular del servidor.
        """
        if cliente in self.clientes:
            indice = self.clientes.index(cliente)  #Encuentra la posición del cliente
            nickname = self.nicknames[indice]  #Obtiene el apodo del cliente
            self.clientes.remove(cliente)  
            self.nicknames.remove(nickname)  
            try:
                cliente.close()  #Cierra el socket del cliente
            except Exception as e:
                print(f"Error al cerrar el socket del cliente: {e}")  #Mensaje de error si ocurre un problema
            #Informa a los demás clientes de la desconexión del usuario
            mensaje = f"[SERVIDOR]: {nickname} se ha desconectado.".encode(ENCODING)
            self.transmitir_mensaje(mensaje, cliente)
            print(f"SERVIDOR: {nickname} se ha desconectado.")  #Notificación en el servidor

    """def recibir_conexion(self):
        """
        #Acepta nuevas conexiones de clientes y configura sus hilos para manejar mensajes.
    """
        while self.running:
            try:
                cliente, address = self.servidor.accept()  #Recibe una nueva conexión
                cliente.send("@nickname".encode(ENCODING))  #Solicita el apodo al cliente
                nickname = cliente.recv(self.buffer_size).decode(ENCODING)  #Recibe el apodo

                if not self.running:
                    cliente.close()  #Cierra el socket si el servidor está cerrándos
                    break

                estado_usuario = self.verificar_usuario(nickname)  #Confirma el estado del usuario en la base de datos

                if estado_usuario == "Conectado":
                    #Informa y cierra la conexión si el usuario ya está conectado
                    cliente.send(f"[SERVIDOR]: El usuario '{nickname}' ya está conectado desde otra consola.".encode(ENCODING))
                    cliente.close()
                else:
                    #Agrega el cliente y su apodo a las listas
                    self.clientes.append(cliente)
                    self.nicknames.append(nickname)
                    print(f"SERVIDOR: {nickname} está conectado desde {address}.")  #Mensaje en el servidor

                    #Informa a los demás usuarios que un nuevo cliente se unió
                    mensaje = f"[SERVIDOR]: {nickname} se unió al chat.".encode(ENCODING)
                    self.transmitir_mensaje(mensaje, cliente)
                    cliente.send("Conectado al servidor.".encode(ENCODING))  #Confirma la conexión al cliente

                    #Inicia un hilo para procesar mensajes del cliente
                    hilo = threading.Thread(target=self.manejar_mensaje, args=(cliente,))
                    hilo.start()
                    self.hilos.append(hilo)  #Añade el hilo a la lista de hilos
            except Exception as e:
                if self.running:
                    print(f"Error al aceptar conexiones: {e}")  #Mensaje de error si ocurre un problema
                break"""
    
    def recibir_conexion(self):
        while self.running:
            try:
                cliente, address = self.servidor.accept()
                cliente.send("@nickname".encode(ENCODING))
                nickname = cliente.recv(self.buffer_size).decode(ENCODING)

                if not self.running:
                    cliente.close()
                    break

                estado_usuario = self.verificar_usuario(nickname)

                if estado_usuario == "Conectado":
                    cliente.send(f"[SERVIDOR]: El usuario '{nickname}' ya está conectado desde otra consola.".encode(ENCODING))
                    cliente.close()
                else:
                    self.clientes.append(cliente)
                    self.nicknames.append(nickname)
                    self.estados.append("disponible")  # Estado inicial del cliente
                    print(f"SERVIDOR: {nickname} está conectado desde {address}.")

                    mensaje = f"[SERVIDOR]: {nickname} se unió al chat.".encode(ENCODING)
                    self.transmitir_mensaje(mensaje, cliente)
                    cliente.send("Conectado al servidor.".encode(ENCODING))

                    hilo = threading.Thread(target=self.manejar_mensaje, args=(cliente,))
                    hilo.start()
                    self.hilos.append(hilo)
            except Exception as e:
                if self.running:
                    print(f"Error al aceptar conexiones: {e}")
                break


    def verificar_usuario(self, nickname):
        """
        Confirma si el usuario existe en la base de datos y actualiza su estado.
        """
        try:
            with self.db.cursor() as cursor:
                #Consulta si el usuario existe en la base de datos
                cursor.execute("SELECT * FROM usuarios WHERE nickname = %s", (nickname,))
                usuario = cursor.fetchone()

                if usuario:
                    if nickname in self.nicknames:
                        return "Conectado"  #El usuario ya está conectado
                    else:
                        
                        cursor.execute("UPDATE usuarios SET connected_at = %s WHERE nickname = %s", (datetime.now(), nickname))
                        self.db.commit()
                        return "Existe"  
                else:
                    #Inserta un nuevo usuario en la base de datos
                    cursor.execute("INSERT INTO usuarios (nickname, connected_at) VALUES (%s, %s)", (nickname, datetime.now()))
                    self.db.commit()
                    return "Nuevo"  
        except Exception as e:
            print(f"Error al verificar el usuario en la base de datos: {e}")  
            return "Error"

    def iniciar(self):
        """
        Inicia el servidor y gestiona los comandos ingresados desde la consola.
        """
        try:
            #Lanza un hilo para manejar conexiones entrantes
            hilo_aceptar_conexiones = threading.Thread(target=self.recibir_conexion)
            hilo_aceptar_conexiones.start()

            #Bucle para leer y ejecutar comandos desde la consola del servidor
            while self.running:
                comando = input('')  #Espera que el usuario escriba un comando
                if comando.lower() == 'salir':
                    print("SERVIDOR: Cerrando el servidor.")  
                    self.running = False  
                    self.servidor.close()  
                    self.desconectar_clientes()  
                    break
        except KeyboardInterrupt:
            #Captura la interrupción de teclado 
            print("SERVIDOR: Interrupción del teclado. Apagando el servidor.")
            self.running = False
            self.servidor.close()
            self.desconectar_clientes()
        finally:
            #Mensaje final y cierre de la conexión a la base de datos
            print("SERVIDOR: Servidor cerrado correctamente.")
            if self.db:
                self.db.close()

def main():
    """
    Función principal que crea una instancia del servidor y la inicia.
    """
    servidor = Servidor()
    servidor.iniciar()

if __name__ == "__main__":
    main()
