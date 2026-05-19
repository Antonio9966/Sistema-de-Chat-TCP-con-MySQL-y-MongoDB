import socket
import threading
import sys

HOST = 'localhost'
PORT = 5000

def recibir_mensajes(client):
    """Hilo para recibir mensajes del servidor de forma continua"""
    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                print(f'\n{data}')
                print('Tu: ', end='', flush=True)
            else:
                break
        except:
            break

def main():
    # Crear socket cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar al servidor
        client.connect((HOST, PORT))
        print(f'Conectado al servidor {HOST}:{PORT}')
        
        # Pedir nombre de usuario
        nombre = input('Ingresa tu nombre: ')
        client.sendall(nombre.encode())
        
        # Crear hilo para recibir mensajes
        t = threading.Thread(target=recibir_mensajes, args=(client,), daemon=True)
        t.start()
        
        print('Conectado al servidor. Escribe mensajes (escribe "salir" para terminar)\n')
        
        # Enviar mensajes
        while True:
            try:
                mensaje = input('Tu: ')
                
                if mensaje.lower() == 'salir':
                    client.sendall('salir'.encode())
                    break
                
                if mensaje:
                    client.sendall(mensaje.encode())
            
            except KeyboardInterrupt:
                print('\nDesconectando...')
                break
            except Exception as e:
                print(f'Error: {e}')
                break
    
    except ConnectionRefusedError:
        print('Error: No se puede conectar al servidor. ¿Está corriendo?')
    except Exception as e:
        print(f'Error de conexión: {e}')
    
    finally:
        client.close()
        print('Desconectado del servidor')
def guardar_mensaje(nombre, contenido):
    if not db_mysql or not cursor:
        return
    try:
        cursor.execute('SELECT id FROM usuarios WHERE nombre = %s', (nombre,))
        usuario = cursor.fetchone()
        
        if usuario:
            id_usuario = usuario[0]
            cursor.execute(
                'INSERT INTO mensajes (id_usuario, contenido) VALUES (%s, %s)',
                (id_usuario, f'{nombre}: {contenido}')
            )
            db_mysql.commit()
        
        if db_mongo:
            db_mongo.usuarios.update_one(
                {'nombre': nombre},
                {'$push': {'mensajes': {'contenido': contenido, 'fecha': datetime.now()}}}
            )
    except Exception as e:
        print(f"Error guardando: {e}")
if __name__ == '__main__':
    main()
