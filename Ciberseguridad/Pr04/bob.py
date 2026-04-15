import funciones_rsa
import funciones_aes
from socket_class import SOCKET_SIMPLE_TCP
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import json

# Cargo la clave pública de Alice y la clave privada de Bob
Pub_A = funciones_rsa.cargar_RSAKey_Publica("./Ciberseguridad/Pr04/keys/rsa_alice.pub")
Pri_B = funciones_rsa.cargar_RSAKey_Privada("./Ciberseguridad/Pr04/keys/rsa_bob.pem", "bob")

# Creamos el servidor para Bob y recibimos las claves y la firma
socketserver = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketserver.escuchar()

K1_cif = socketserver.recibir()
K2_cif = socketserver.recibir()
K1K2_fir = socketserver.recibir()

# Descifro las claves K1 y K2 con Pri_B
K1 = funciones_rsa.descifrarRSA_OAEP_BIN(K1_cif, Pri_B)
K2 = funciones_rsa.descifrarRSA_OAEP_BIN(K2_cif, Pri_B)

# Compruebo la validez de la firma con Pub_A
if funciones_rsa.comprobarRSA_PSS(K1+K2,K1K2_fir,Pub_A):
    print("Firma de K1||K2 válida")
else:
    print("Firma de K1||K2 NO válida")

#####################
#####################

# Recibo el mensaje, junto con el nonce del AES CTR, y el mac del HMAC
nonce = socketserver.recibir()
mensajeCifrado = socketserver.recibir()
MAC = socketserver.recibir()

# Verifico el mac
hmac_alice_obj = HMAC.new(K2, digestmod=SHA256)
hmac_alice_obj.update(mensajeCifrado)
try:
    hmac_alice_obj.verify(MAC)
    print("Verificación HMAC de Alice: OK")
except ValueError:
    print("Error: HMAC de Alice NO es válido")
    exit(1)


# Descifro el mensaje
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, nonce)
mensajeDescifradoAlice = funciones_aes.descifrarAES_CTR(aes_descifrado, mensajeCifrado)
mensajeAlice = json.loads(mensajeDescifradoAlice.decode("utf-8"))


# Visualizo la identidad del remitente
print("Identidad del remitente:", mensajeAlice[0])
nA_hex = mensajeAlice[1]
print("Nonce nA:", nA_hex)

#####################
#####################

# Genero el json con el nombre de Bob, el de Alice y el nonce nA
mensajeBob = ["Bob", "Alice", nA_hex]
jStr_bob = json.dumps(mensajeBob)

# Cifro el json con K1
aes_cifrado, nonce_ini = funciones_aes.iniciarAES_CTR_cifrado(K1)
mensajeCifradoBob = funciones_aes.cifrarAES_CTR(aes_cifrado, jStr_bob.encode("utf-8"))

# Aplico HMAC
hmac = HMAC.new(K2, digestmod=SHA256)
hmac.update(mensajeCifradoBob)
MAC_bob = hmac.digest()


# Envío el json cifrado junto con el nonce del AES CTR, y el mac del HMAC
socketserver.enviar(nonce_ini)
socketserver.enviar(mensajeCifradoBob)
socketserver.enviar(MAC_bob)

#####################
#####################

# Recibo el primer mensaje de Alice
mensajeCifrado1 = socketserver.recibir()
MAC_1 = socketserver.recibir()

# Verifico el mac
hmac_1 = HMAC.new(K2, digestmod=SHA256)
hmac_1.update(mensajeCifrado1)
try:
    hmac_1.verify(MAC_1)
    print("Verificación HMAC Mensaje 1 de Alice: OK")
except ValueError:
    print("Error: HMAC Mensaje 1 de Alice NO es válido")

# Descifro el mensaje
mensajeDescifrado1 = funciones_aes.descifrarAES_CTR(aes_descifrado, mensajeCifrado1)

# Muestro el mensaje
mensaje1 = json.loads(mensajeDescifrado1.decode("utf-8"))
print("Mensaje 1 de Alice:", mensaje1[0])

# Recibo el segundo mensaje de Alice
mensajeCifrado2 = socketserver.recibir()
MAC_2 = socketserver.recibir()

# Verifico el mac
hmac_2 = HMAC.new(K2, digestmod=SHA256)
hmac_2.update(mensajeCifrado2)
try:
    hmac_2.verify(MAC_2)
    print("Verificación HMAC Mensaje 2 de Alice: OK")
except ValueError:
    print("Error: HMAC Mensaje 2 de Alice NO es válido")

# Descifro el mensaje 
mensajeDescifrado2 = funciones_aes.descifrarAES_CTR(aes_descifrado, mensajeCifrado2)

# Muestro el mensaje
mensaje2 = json.loads(mensajeDescifrado2.decode("utf-8"))
print("Mensaje 2 de Alice:", mensaje2[0])

# Cierro el socket
socketserver.cerrar()
