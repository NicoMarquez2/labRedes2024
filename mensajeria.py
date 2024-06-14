import sys
import socket
import hashlib
import threading
import time
from datetime import datetime
import signal
import select
import os
# Define una función de manejador para la señal SIGINT
salir = False
def sigint_handler(signum, frame):
    global salir
    salir = True

def obtener_input(timeout):
    inputs, _, _ = select.select([sys.stdin], [], [], timeout)
    if inputs:
        return sys.stdin.readline().strip()
    else:
        return None

# Asigna el manejador para la señal SIGINT y SIGTERM
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

# Guarda los parametros en consola
msg_port= int(sys.argv[1])
auth_ip=sys.argv[2]
auth_port=int(sys.argv[3])

chunk_tamano=1024
# Crea el socket 
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se conecta a traves del socket a esas variables
client_socket.connect((auth_ip,auth_port))

# Recive y guarda el mensaje
msg= client_socket.recv(1024).decode('utf-8').strip()

# Chequea si el mensaje recivido es el correcto para contiunar
if msg != "Redes 2024 - Laboratorio - Autenticacion de Usuarios":
        print("Conexion Incorrecta")
        exit

# Le solicita al usuario el usuario y lo guarda en user
user= input("Digitar Usuario: ")

# Le solicita al usuario la contraseña , lo guarda en pwd y demas lo encripta en md5
pwd= input("Digitar Contrasena: ")
pwd_md5 = hashlib.md5()
pwd_md5.update(pwd.encode('utf-8'))
pwd_md5 = pwd_md5.hexdigest()

# Crea el mensaje que va a enviar para que lo entienda el auth
msg=user + "-" + pwd_md5 + "\n\n" 

# envia el msg 
client_socket.send(msg.encode())

# recive la respuesta 
respuesta= client_socket.recv(1024).decode('utf-8').strip()

# Chequea si la respuesta es correcta 
if respuesta == "NO":
    print("USUARIO INCORRECTO")
    sys.exit()
elif respuesta != "SI":
    print("ERROR PROTOCOLO")
    sys.exit()
else:
    usr=client_socket.recv(1024).decode('utf-8').strip()
    print("Bienvenido " + usr)

#Cierra el socket
client_socket.close()

#Defino proceso emisor
def emisor():
    while not salir:
        if salir:
            break
        msg = obtener_input(1)
        if msg is None:  # No se recibió entrada
            continue
        else:
            ip, mensaje = msg.split(' ', 1)
            if ("&file" in mensaje):
                operacion,archivo= mensaje.split(' ', 1)
                archivo_b= open(archivo, "rb")
                tamano_archivo= os.path.getsize(archivo)
                if ip == "*":
                    while True:
                        chunk = archivo_b.read(chunk_tamano)  
                        if not chunk:
                            break
                        emisor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        ip_receptor = ('<broadcast>', msg_port)
                        msg= b'&file' + b' ' + archivo.encode('utf-8') + b' ' + chunk
                        emisor_socket.sendto(msg, ip_receptor)
                    msg= b'&file' + b' ' + archivo.encode('utf-8') + b' ' + b'Final'
                    emisor_socket.sendto(msg, ip_receptor)
                    emisor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
                else:
                    print()
            else:
                if ip == "*":
                    emisor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    mensaje = f"{user} dice: {mensaje}"
                    ip_receptor = ('<broadcast>', msg_port)
                    emisor_socket.sendto(mensaje.encode("utf-8"), ip_receptor)
                    emisor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
                else:
                    ip_r = socket.gethostbyname(ip)
                    ip_receptor = (ip_r, msg_port)
                    mensaje = f"{user} dice: {mensaje}"
                    emisor_socket.sendto(mensaje.encode("utf-8"), ip_receptor)
                    time.sleep(1)

#Defino proceso receptor
def receptor():
    while not salir:
        if salir:
            break
        msg, adress = emisor_socket.recvfrom(1024)
        mensaje = msg.decode("utf-8")
        if "&file" in mensaje:
            tipo,msg = mensaje.split(' ', 1)
            archivo,chunk=msg.split(' ', 1)
            archivo_destino_abierto = open(archivo, 'wb')
            if(chunk != "Final"):
                chunk2= chunk.encode("utf-8")
                archivo_destino_abierto.write(chunk2)
            else:
                archivo_destino_abierto.close()
        else:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
            if mensaje == "5eb379cd7ffa79b66cc5007c0cf4ae67":
                print("\rCTRL+C recibido... Cerrando sesion")
            else:
                print(f"[{fecha}] {adress[0]} {mensaje}")

emisor_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
emisor_socket.bind(('', msg_port))

# Crear procesos para receptor y emisor
proceso_emisor = threading.Thread(target=emisor)
proceso_receptor = threading.Thread(target=receptor)

# Iniciar los procesos
proceso_receptor.start()
proceso_emisor.start()
#While que detiene al proceso Principal
while (not salir):
    time.sleep(1)
    if salir:
        break

ip_receptor = ("localhost", msg_port)
emisor_socket.sendto("5eb379cd7ffa79b66cc5007c0cf4ae67".encode("utf-8"), ip_receptor)
proceso_receptor.join(timeout= 1)
proceso_emisor.join(timeout= 1)
emisor_socket.close()
sys.exit()
#client_socket.close()
