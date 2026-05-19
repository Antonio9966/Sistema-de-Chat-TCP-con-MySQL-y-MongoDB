# PRÁCTICA 3: SISTEMA DE CHAT TCP CON MYSQL Y MONGODB

## 📋 Descripción
Sistema de chat en tiempo real desarrollado en Python que demuestra:
- **Sockets TCP/IP** para comunicación en red
- **Threading** para múltiples clientes simultáneos
- **MySQL 8** para persistencia relacional
- **MongoDB 7** para persistencia documental
- **Git/GitHub** para control de versiones

## 📁 Archivos Incluidos

### Documentos
- **Practica3_Chat_TCP_MySQL_MongoDB.docx** - Documento Word con la práctica paso a paso con espacios para capturas
- **GUIA_RAPIDA.txt** - Guía rápida de instalación y ejecución
- **EXPLICACION_CODIGOS.txt** - Explicación línea por línea de ambos códigos
- **CHEAT_SHEET.txt** - Referencia de comandos importantes

### Código
- **server.py** - Servidor TCP multiusuario con conexión a ambas BD
- **client.py** - Cliente TCP para conectarse al servidor

## 🚀 Inicio Rápido

### 1. Instalación
```bash
sudo apt update
sudo apt install python3 python3-venv python3-full mysql-server mongodb git -y
```

### 2. Configurar MySQL
```bash
sudo service mysql start
sudo mysql

CREATE DATABASE chat_db;
USE chat_db;
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE mensajes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT,
  contenido TEXT,
  fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
exit
```

### 3. Configurar MongoDB
```bash
sudo service mongodb start
mongosh

use chat_db
db.usuarios.insertOne({
  nombre: 'Test',
  email: 'test@email.com',
  mensajes: []
})
exit
```

### 4. Crear Entorno Python
```bash
mkdir socket_project && cd socket_project
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python pymongo
```

### 5. Copiar Archivos
```bash
# Copiar server.py y client.py a ~/socket_project
```

### 6. Ejecutar Sistema

**Terminal 1 (Servidor):**
```bash
cd ~/socket_project
source venv/bin/activate
sudo service mysql start
sudo service mongodb start
python3 server.py
```

**Terminal 2 (Cliente 1):**
```bash
cd ~/socket_project
source venv/bin/activate
python3 client.py
# Ingresa tu nombre: Alex
```

**Terminal 3 (Cliente 2):**
```bash
cd ~/socket_project
source venv/bin/activate
python3 client.py
# Ingresa tu nombre: Juan
```

### 7. Verificar Datos

**En MySQL:**
```bash
mysql -u root -p1234
USE chat_db;
SELECT * FROM usuarios;
SELECT * FROM mensajes;
exit
```

**En MongoDB:**
```bash
mongosh
use chat_db
db.usuarios.find().pretty()
exit
```

## 🔧 Características del Código

### Server.py
- ✅ Escucha en puerto 5000
- ✅ Acepta múltiples clientes con threading
- ✅ Guarda mensajes en MySQL automáticamente
- ✅ Guarda mensajes en MongoDB automáticamente
- ✅ Reenvía mensajes a otros clientes en tiempo real
- ✅ Notifica conexiones/desconexiones

### Client.py
- ✅ Se conecta a servidor en localhost:5000
- ✅ Pide nombre de usuario
- ✅ Recibe mensajes en hilo separado
- ✅ Envía mensajes de forma interactiva
- ✅ Comando 'salir' para desconectar

## 📊 Flujo de Datos

```
Cliente 1              Servidor              Cliente 2
  │                      │                      │
  ├──── Conecta ────────▶│                      │
  │                      ├──── Crea Usuario ──▶│ (MySQL/MongoDB)
  │                      │                      │
  │                      ├──── Notifica ──────▶│
  │                      │                  "Cliente 1 conectó"
  │                      │                      │
  ├──── Conecta ────────▶│                      │
  │                      ├──── Crea Usuario ──▶│ (MySQL/MongoDB)
  │                      │                      │
  ├──── "Hola" ────────▶│                      │
  │                      ├──── Guarda en BD ──▶│
  │                      │                      │
  │                      ├──── Envía ────────▶│
  │                      │                  "Cliente1: Hola"
  │                      │                      │
  │                      │◀──── "Qué tal" ────┤
  │                      ├──── Guarda en BD ──▶│
  │                      │                      │
  │◀──── Envía ─────────┤                      │
  │    "Cliente2: Qué tal"                     │
```

## 🗄️ Estructura de Datos

### MySQL (Relacional)
```
usuarios
├── id (PK)
├── nombre
├── email (UNIQUE)
└── fecha_creacion

mensajes
├── id (PK)
├── id_usuario (FK)
├── contenido
└── fecha_envio
```

### MongoDB (Documental)
```
{
  "_id": ObjectId(...),
  "nombre": "Alex",
  "email": "alex@email.com",
  "mensajes": [
    {
      "contenido": "Hola",
      "fecha": ISODate("2026-05-...")
    }
  ]
}
```

## 📝 Conceptos Aprendidos

1. **Sockets TCP/IP** - Comunicación cliente-servidor
2. **Threading** - Multihilo para clientes simultáneos
3. **MySQL** - Base de datos relacional con transacciones
4. **MongoDB** - Base de datos documental con inserción flexible
5. **Python** - Lenguaje de programación del sistema
6. **Git** - Control de versiones y colaboración

## 🐛 Solución de Problemas

### "Port already in use"
```bash
lsof -i :5000
kill -9 <PID>
```

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install mysql-connector-python pymongo
```

### "Can't connect to MySQL socket"
```bash
sudo service mysql start
```

### "Connection refused"
- Verificar que servidor esté corriendo en Terminal 1
- Verificar que HOST y PORT sean correctos

## 📚 Documentación Adicional

Ver los siguientes archivos para más detalles:
- `GUIA_RAPIDA.txt` - Instrucciones paso a paso
- `EXPLICACION_CODIGOS.txt` - Análisis detallado del código
- `CHEAT_SHEET.txt` - Referencia de comandos

## 🎯 Objetivos Alcanzados

✅ Sistema de chat funcional en tiempo real
✅ Múltiples clientes conectados simultáneamente
✅ Persistencia de datos en MySQL (relacional)
✅ Persistencia de datos en MongoDB (documental)
✅ Control de versiones con Git
✅ Código comentado y bien estructurado

## 📌 Notas Importantes

- Puerto 5000 es de desarrollo, cambiar para producción
- Contraseña '1234' es solo para desarrollo
- Sin contraseña configurada = usar `sudo mysql`
- El servidor debe estar corriendo antes de conectar clientes
- Ambas bases de datos se actualizan simultáneamente

## 👨‍💻 Autor
Antonio Guerrero - Mayo 2026
Universidad Politécnica Estatal del Carchi

## 📄 Licencia
Este proyecto es para propósitos educativos.

---

Para ejecutar la práctica completa, seguir los pasos del archivo `GUIA_RAPIDA.txt`

