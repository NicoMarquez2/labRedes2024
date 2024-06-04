import sys
import socket
import hashlib
import multiprocessing
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

#Defino proceso emisor, le paso como argumentos el mensaje a enviar
def emisor():
    emisor_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    emisor_socket.bind(('', msg_port))
    ip = "127.0.0.1"
    while True:
        msg = input()
        print(msg)
        emisor_socket.sendto(msg.encode("utf-8"), ip)
        time.sleep(1)

 #   print()
 #   print(msg)
 #   indice_espacio = msg.find(" ")

    # Extraer la IP y el resto del mensaje
#    ip = msg[:indice_espacio]
#    resto_mensaje = msg[indice_espacio+1:]
#    print("Dirección IP:", ip)
#    print("Resto del mensaje:", resto_mensaje)
#    emisor_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    while True:
#        emisor_socket.connect((ip, msg_port))
#        time.sleep(1)
#        fecha_actual = time.strftime("%Y-%m-%d %H:%M")
#        mensaje = msg_emisor + fecha_actual
#        emisor_socket.send(mensaje.encode())


def receptor():
    receptor_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receptor_socket.bind(('', msg_port))

#    nombre_host = socket.gethostname()
#    ip =socket.gethostbyname(nombre_host)

#    receptor_socket.listen(5)
    while True:
#        emisor_socket, emisor_address = receptor_socket.accept()
        msg = receptor_socket.recvfrom(1024)
        print(msg)
#        receptor_socket.close()


print("ASASASDD")

#msg_emisor = input("escriba su mensaje: ")

# Crear procesos para receptor y emisor
#proceso_receptor = multiprocessing.Process(target=receptor)
#proceso_emisor = multiprocessing.Process(target=emisor)
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
