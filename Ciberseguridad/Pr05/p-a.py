
from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################
print('Leyendo la clave KAT')
KAT= open("KAT.bin", "rb").read()

# (A realizar por el alumno/a...)

# Paso 3) A->T: KAT(Alice, Na) en AES-GCM
#########################################

# Crear el socket de conexion con T (5552)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5552)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16)

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
msg_TE = []
msg_TE.append("Alice")
msg_TE.append(t_n_origen.hex())
json_ET = json.dumps(msg_TE)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KAT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_ET.encode("utf-8"))

# Envia los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)

# Paso 4) T->A: KAT(K1, K2, Na) en AES-GCM
##########################################

# Se reciben los datos de T
cifrado = socket.recibir()
cifrado_mac = socket.recibir()
cifrado_nonce = socket.recibir()

# Desciframos los datos con AES GCM
datos_descifrados_TA = funciones_aes.descifrarAES_GCM(KAT, cifrado_nonce,cifrado, cifrado_mac)

# Extraemos las claves del mensaje y el nonce
json_TA = datos_descifrados_TA.decode('utf-8', 'ignore')
print('T -> A mensaje descifrado:' + json_TA)
mensaje_TA = json.loads(json_TA)
K1, K2, nonce = mensaje_TA

# Comprobamos que el nonce recibido es el mismo que el enviado
if nonce != t_n_origen.hex():
    print("Error: el nonce recibido no coincide con el enviado")
    sys.exit(1)
else:
    print("Nonce recibido coincide con el enviado")

# Guardamos las claves K1 y K2 
K1 = bytearray.fromhex(K1)
K2 = bytearray.fromhex(K2)

# Cerramos la conexión con T
socket.cerrar()

# Paso 5) A->B: KAB(Nombre) en AES-CTR con HMAC
###############################################

# Conectamos con B (5553)
print("Creando conexion con B...")
socket_Bob = SOCKET_SIMPLE_TCP('127.0.0.1', 5553)
socket_Bob.conectar()

json_AB = json.dumps("Alice").encode('utf-8')

# Ciframos los datos con AES CTR con la clave K1
aes_cifrado, nonce_cifrado = funciones_aes.iniciarAES_CTR_cifrado(K1)
mensaje_Cifrado_AB = funciones_aes.cifrarAES_CTR(aes_cifrado, json_AB)

# Calculamos el HMAC del mensaje cifrado con la clave K2
hmac_AB = HMAC.new(K2, mensaje_Cifrado_AB, digestmod=SHA256)
mac = hmac_AB.digest()

# Enviamos el mensaje cifrado y el HMAC a B
socket_Bob.enviar(mensaje_Cifrado_AB)
socket_Bob.enviar(mac)
socket_Bob.enviar(nonce_cifrado)

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

# Recibimos el mensaje de B
cifrado = socket_Bob.recibir()
cifrado_mac = socket_Bob.recibir()
cifrado_nonce = socket_Bob.recibir()    

# Verificamos el HMAC del mensaje cifrado con la clave K2
hmac_calculado = HMAC.new(K2, cifrado, digestmod=SHA256)
try:
    hmac_calculado.verify(cifrado_mac)
    print("HMAC verificado correctamente")
except ValueError:
    print("Error: HMAC no verificado")
    sys.exit(1)

# Desciframos los datos con AES CTR con la clave K1
datos_descifrados = funciones_aes.descifrarAES_CTR(funciones_aes.iniciarAES_CTR_descifrado(K1, cifrado_nonce), cifrado)
apellido_recibido = datos_descifrados.decode('utf-8')
print("Apellido recibido de B: " + apellido_recibido)

# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

# Ciframos el mensaje "END" con AES CTR con la clave K1
json_END = json.dumps("END").encode('utf-8')
aes_cifrado, nonce_cifrado = funciones_aes.iniciarAES_CTR_cifrado(K1)
mensaje_Cifrado_END = funciones_aes.cifrarAES_CTR(aes_cifrado, json_END)

# Calculamos el HMAC del mensaje cifrado con la clave K2
hmac_END = HMAC.new(K2, mensaje_Cifrado_END, digestmod=SHA256)
mac_END = hmac_END.digest()

# Enviamos el mensaje cifrado y el HMAC a B
socket_Bob.enviar(mensaje_Cifrado_END)
socket_Bob.enviar(mac_END)
socket_Bob.enviar(nonce_cifrado)

# Cerramos la conexión con B
socket_Bob.cerrar()
print("Fin de la comunicación con B")
