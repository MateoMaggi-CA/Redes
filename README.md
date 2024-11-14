Chat Cliente-Servidor 🖥️💬

Este proyecto es una aplicación de chat basada en un sistema cliente-servidor desarrollado en Python 🐍. La aplicación permite a múltiples clientes conectarse a un servidor central y comunicarse en tiempo real, incluyendo funcionalidades para gestionar estados de usuario.

Funcionalidades 🚀

Cliente 🧑‍💻

Conexión al servidor: El cliente se conecta a una IP y un puerto especificados y puede enviar y recibir mensajes.

Cambiar el estado: Los clientes pueden cambiar su estado usando el comando /estado <estado>, lo que permite informar si están disponibles, ocupados, o ausentes. 

Listar usuarios conectados: Permite ver todos los usuarios conectados al servidor y su estado actual con el comando /listar.

Mensajes públicos y privados: Los clientes pueden enviar mensajes públicos a todos los usuarios y mensajes privados usando !usuario.

Perfil de usuario: Al ingresar el comando /perfil, el cliente puede solicitar información sobre su perfil, como su ID y la última conexión.

Desconectar: Los usuarios pueden desconectarse del chat y cerrar la aplicación con /salir o /desconectar.

Servidor 🖧

Gestión de clientes: El servidor acepta múltiples conexiones de clientes y mantiene una lista de los usuarios conectados.

Almacenamiento en MySQL: La aplicación se conecta a una base de datos MySQL donde se almacenan los datos de los usuarios.

Transmisión de mensajes: Envía mensajes a todos los clientes conectados o al destinatario específico en el caso de mensajes privados.

Gestión de estados: Registra y actualiza el estado de cada cliente, mostrándolo a los demás en la lista de usuarios.

Desconexión de clientes: Gestiona la desconexión de usuarios y mantiene actualizada la lista de usuarios conectados.

Comandos Disponibles 📜

/estado <estado>: Cambia el estado del usuario (por ejemplo: /estado ocupado).

/listar: Muestra la lista de usuarios conectados y su estado.

/perfil: Solicita información del perfil del usuario.

/desconectar o /salir: Desconecta al usuario del servidor y cierra la aplicación.

Ejemplo de Uso 📖

Inicia el servidor ejecutando servidor.py:

Inicia uno o más clientes ejecutando cliente.py y proporcionando un nombre de usuario cuando se solicite:

En el cliente, utiliza los comandos disponibles para interactuar con otros usuarios.

Requisitos 📦
Python 3.6 o superior.
Biblioteca pymysql para la conexión con la base de datos.
Servidor MySQL configurado con una base de datos para almacenar los datos de usuario.

Para instalar las dependencias, podes usar:

pip install pymysql

Instalación y Configuración 🔧
Clona este repositorio en tu máquina local:

git clone https://github.com/MateoMaggi-CA/Redes

Configura tu base de datos MySQL:

Crea una base de datos llamada Redes.
Configura las credenciales en el archivo servidor.py.
Ejecuta el servidor y despues los clientes. Los clientes podrán comunicarse entre sí a través del servidor.


