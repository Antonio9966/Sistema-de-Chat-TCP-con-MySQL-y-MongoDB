import socket
import threading
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000
clientes = []

# Conexión MySQL
try:
    db_mysql = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='chat_db'
    )
    cursor = db_mysql.cursor()
    print("✓ MySQL conectado")
except Exception as e:
    print(f"✗ Error MySQL: {e}")
    db_mysql = None
    cursor = None

# Conexión MongoDB
try:
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db_mongo = mongo_client['chat_db']
    print("✓ MongoDB conectado")
except Exception as e:
    print(f"✗ Error MongoDB: {e}")
    db_mongo = None

def guardar_mensaje(nombre, contenido):
    """Guarda el mensaje en MySQL y MongoDB"""
    try:
        # Guardar en MySQL
        cursor.execute('SELECT id FROM usuarios WHERE nombre = %s', (nombre,))
        usuario = cursor.fetchone()
        
        if usuario:
            id_usuario = usuario[0]
            cursor.execute(
                'INSERT INTO mensajes (id_usuario, contenido) VALUES (%s, %s)',
                (id_usuario, f'{nombre}: {contenido}')
            )
            db_mysql.commit()
        
        # Guardar en MongoDB
        db_mongo.usuarios.update_one(
            {'nombre': nombre},
            {'$push': {'mensajes': {'contenido': contenido, 'fecha': datetime.now()}}}
        )
    except Exception as e:
        print(f'Error al guardar mensaje: {e}')

def manejar_cliente(conn, addr):
    """Maneja la conexión de cada cliente en un hilo separado"""
    print(f'Nuevo cliente conectado: {addr}')
    
    try:
        # Recibir nombre del cliente
        nombre = conn.recv(1024).decode()
        
        # Crear usuario en MySQL si no existe
        cursor.execute('SELECT id FROM usuarios WHERE nombre = %s', (nombre,))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO usuarios (nombre, email) VALUES (%s, %s)',
                (nombre, f'{nombre.lower()}@email.com')
            )
            db_mysql.commit()
        
        # Crear documento en MongoDB si no existe
        if not db_mongo.usuarios.find_one({'nombre': nombre}):
            db_mongo.usuarios.insert_one({
                'nombre': nombre,
                'email': f'{nombre.lower()}@email.com',
                'mensajes': []
            })
        
        clientes.append((conn, nombre))
        print(f'{nombre} se ha conectado desde {addr}')
        
        # Notificar a otros clientes
        mensaje_conexion = f'*** {nombre} se ha conectado al chat ***'
        for c, n in clientes:
            if c != conn:
                c.sendall(mensaje_conexion.encode())
        
        # Recibir mensajes del cliente
        while True:
            data = conn.recv(1024).decode()
            
            if not data or data.lower() == 'salir':
                break
            
            # Guardar en bases de datos
            guardar_mensaje(nombre, data)
            
            # Mensaje completo
            mensaje = f'{nombre}: {data}'
            print(f'[{addr}] {mensaje}')
            
            # Enviar a otros clientes
            for c, n in clientes:
                if c != conn:
                    c.sendall(mensaje.encode())
    
    except Exception as e:
        print(f'Error con cliente {addr}: {e}')
    
    finally:
        # Eliminar cliente de la lista
        clientes.remove((conn, nombre))
        conn.close()
        print(f'{nombre} se ha desconectado')
        
        # Notificar desconexión
        mensaje_desconexion = f'*** {nombre} se ha desconectado del chat ***'
        for c, n in clientes:
            c.sendall(mensaje_desconexion.encode())

# Crear socket servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f'Servidor multiusuario escuchando en {HOST}:{PORT}...')
print('Esperando conexiones...\n')

try:
    while True:
        conn, addr = server.accept()
        # Crear hilo para cada cliente
        t = threading.Thread(target=manejar_cliente, args=(conn, addr))
        t.daemon = True
        t.start()
except KeyboardInterrupt:
    print('\nServidor detenido')
finally:
    server.close()
