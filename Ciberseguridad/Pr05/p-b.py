

from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################

# Lee clave KBT
KBT = open("KBT.bin", "rb").read()

# Paso 1) B->T: KBT(Bob, Nb) en AES-GCM
#######################################

# Crear el socket de conexion con T (5551)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16)

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
msg_TE = []
msg_TE.append("Bob")
msg_TE.append(t_n_origen.hex())
json_ET = json.dumps(msg_TE)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KBT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_ET.encode("utf-8"))

# Envia los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)
print("PASO 1: Datos enviados desde B a T")

# Paso 2) T->B: KBT(K1, K2, Nb) en AES-GCM
##########################################

# Recibimos los datos de T
cifrado = socket.recibir()
cifrado_mac = socket.recibir()
cifrado_nonce = socket.recibir()
print("PASO 2: Datos recibidos de T a B")

# Desciframos los datos con AES GCM
datos_descifrados_TB = funciones_aes.descifrarAES_GCM(KBT, cifrado_nonce,cifrado, cifrado_mac)

# Extraemos la información del mensaje
json_TB = datos_descifrados_TB.decode('utf-8', 'ignore')
mensaje_TB = json.loads(json_TB)
K1, K2, nonce = mensaje_TB

# Comprobamos que el nonce recibido es el mismo que el enviado
if t_n_origen.hex() != nonce:
    print("Error: el nonce recibido no coincide con el enviado")
    sys.exit(1) 
else:
    print("Nonce recibido coincide con el enviado")

#Guardamos las claves K1 y K2
K1 = bytearray.fromhex(K1)
K2 = bytearray.fromhex(K2)

# Cerramos el socket entre B y T
socket.cerrar()

# Paso 5) A->B: KAB(Nombre) en AES-CTR con HMAC
###############################################

# Se espera a Alice en el socket de escucha (5553)
print("Esperando a Alice...")
socket_Alice = SOCKET_SIMPLE_TCP('127.0.0.1', 5553)
socket_Alice.escuchar()

# Recibe el mensaje
cifrado = socket_Alice.recibir()
cifrado_mac = socket_Alice.recibir()
cifrado_nonce = socket_Alice.recibir()
print("PASO 5: Datos recibidos desde A por B")

# Se verifica la integridad del mensaje con HMAC
hmac_calculado = HMAC.new(K2, cifrado, digestmod=SHA256)
try:
    hmac_calculado.verify(cifrado_mac)
    print("HMAC verificado correctamente")
except ValueError:
    print("Error: HMAC no verificado")
    sys.exit(1)

# Descifro los datos con AES CTR
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, cifrado_nonce)
datos_descifrado = funciones_aes.descifrarAES_CTR(aes_descifrado, cifrado)
nombre_recibido = datos_descifrado.decode('utf-8', 'ignore')
print("Nombre recibido de Alice: " + nombre_recibido)

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

# Cifra los datos con AES CTR
json_Apellido = json.dumps("Apellido").encode('utf-8')
aes_cifrado, nonce_cifrado = funciones_aes.iniciarAES_CTR_cifrado(K1)
cifrado_Apellido = funciones_aes.cifrarAES_CTR(aes_cifrado, json_Apellido)

# Calcula el HMAC del mensaje cifrado
hmac_calculado = HMAC.new(K2, msg=cifrado_Apellido, digestmod=SHA256)
mac = hmac_calculado.digest()

# Envia los datos a Alice
socket_Alice.enviar(cifrado_Apellido)
socket_Alice.enviar(mac)
socket_Alice.enviar(nonce_cifrado)  
print("PASO 6: Datos enviados desde B a A")

# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

# Recibe el mensaje
cifrado = socket_Alice.recibir()
cifrado_mac = socket_Alice.recibir()
cifrado_nonce = socket_Alice.recibir()
print("PASO 7: Datos recibidos desde A por B")

# Se verifica la integridad del mensaje con HMAC
hmac_calculado = HMAC.new(K2, cifrado, digestmod=SHA256)
try:
    hmac_calculado.verify(cifrado_mac)
    print("HMAC verificado correctamente")
except ValueError:
    print("Error: HMAC no verificado")
    sys.exit(1)

# Descifro los datos con AES CTR
mensaje_descifrado = funciones_aes.descifrarAES_CTR(funciones_aes.iniciarAES_CTR_descifrado(K1, cifrado_nonce), cifrado)
mensaje = json.loads(mensaje_descifrado.decode('utf-8'))
print("Mensaje recibido de Alice: " + mensaje)

# Cerramos el socket entre B y A
socket_Alice.cerrar()
