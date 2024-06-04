import sys
import socket
import hashlib
import threading
import time

# Guarda los parametros en consola 
msg_port= int(sys.argv[1])
auth_ip=sys.argv[2]
auth_port=int(sys.argv[3])

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
print("sigue")

#Cierra el socket
client_socket.close()

#Defino proceso emisor
def emisor():
    ip = ("127.0.0.1", msg_port)
    while True:
        msg = input()
        print(msg)
        emisor_socket.sendto(msg.encode("utf-8"), ip)
        time.sleep(1)

#Defino proceso receptor
def receptor():
    while True:
        msg = emisor_socket.recvfrom(1024)
        print(msg)

emisor_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
emisor_socket.bind(('', msg_port))

# Crear procesos para receptor y emisor
proceso_emisor = threading.Thread(target=emisor)
proceso_receptor = threading.Thread(target=receptor)
print("2")
# Iniciar los procesos
proceso_receptor.start()
proceso_emisor.start()
print("3")

while True:
     time.sleep(1)
#client_socket.close()
