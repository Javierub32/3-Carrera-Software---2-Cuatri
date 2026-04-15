import funciones_rsa
import funciones_aes
from socket_class import SOCKET_SIMPLE_TCP
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import json

# Cargo la clave pública de Bob y la clave privada de Alice
Pub_B = funciones_rsa.cargar_RSAKey_Publica("./Ciberseguridad/Pr04/keys/rsa_bob.pub")
Pri_A = funciones_rsa.cargar_RSAKey_Privada("./Ciberseguridad/Pr04/keys/rsa_alice.pem", "alice")

# Genero las dos claves
K1 = funciones_aes.crear_AESKey()
K2 = funciones_aes.crear_AESKey()



# Cifro K1 y K2 con Pub_B
K1_cif = funciones_rsa.cifrarRSA_OAEP_BIN(K1, Pub_B)
K2_cif = funciones_rsa.cifrarRSA_OAEP_BIN(K2, Pub_B)

# Firmo la concatenación de K1 y K2 con Pri_A
K1K2_fir = funciones_rsa.firmarRSA_PSS(K1 + K2, Pri_A)

# Conectamos con el servidor y enviamos a Bob a través del socket
socketclient = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketclient.conectar()

socketclient.enviar(K1_cif)
socketclient.enviar(K2_cif)
socketclient.enviar(K1K2_fir)


#####################
#####################


# Genero el json con el nombre de Alice y un nonce nA
nA = get_random_bytes(16)
nA_hex = nA.hex()
mensaje = []
mensaje.append("Alice")
mensaje.append(nA_hex)
jStr = json.dumps(mensaje)

# Cifro el json con K1
aes, nonce = funciones_aes.iniciarAES_CTR_cifrado(K1)
mensajeCifradoAlice = funciones_aes.cifrarAES_CTR(aes, jStr.encode("utf-8"))

# Aplico HMAC
hmac_obj = HMAC.new(K2, digestmod=SHA256)
hmac_obj.update(mensajeCifradoAlice)
MAC_Alice = hmac_obj.digest()

# Envío el json cifrado junto con el nonce del AES CTR, y el mac del HMAC
socketclient.enviar(nonce)
socketclient.enviar(mensajeCifradoAlice)
socketclient.enviar(MAC_Alice)

#####################
#####################

# Recibo el mensaje, junto con el nonce del AES CTR, y el mac del HMAC
nonce_ini_bob = socketclient.recibir()
mensajeCifradoBob = socketclient.recibir()
MAC_bob = socketclient.recibir()

# Verifico el mac
hmac_bob_obj = HMAC.new(K2, digestmod=SHA256)
hmac_bob_obj.update(mensajeCifradoBob)
try:
    hmac_bob_obj.verify(MAC_bob)
    print("Verificación HMAC de Bob: OK")
except ValueError:
    print("Error: HMAC de Bob NO es válido")
    exit(1)

# Descifro el mensaje
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, nonce_ini_bob)
jStr_bob = funciones_aes.descifrarAES_CTR(aes_descifrado, mensajeCifradoBob)
mensajeBob = json.loads(jStr_bob.decode("utf-8"))


# Visualizo la identidad del remitente y compruebo si los campos enviados son los mismo que los recibidos
print("Identidad del remitente:", mensajeBob[0])
if mensajeBob[1] == "Alice" and mensajeBob[2] == nA_hex:
    print("Los campos (nombre y nonce) coinciden con los enviados.")
else:
    print("Los campos recibidos no coinciden.")
    
#####################
#####################

# Intercambio de información NUMERO 1. Al utilizar K1, reutilizo el canal de comunicaciones aes_cifrado
mensaje1 = ["Hola Amigos"]
jStr_1 = json.dumps(mensaje1)
mensajeCifrado1 = funciones_aes.cifrarAES_CTR(aes, jStr_1.encode("utf-8"))

# Aplico HMAC
hmac_1 = HMAC.new(K2, digestmod=SHA256)
hmac_1.update(mensajeCifrado1)
MAC_1 = hmac_1.digest()

# Envío el json cifrado junto con el nonce del AES CTR, y el mac del HMAC
socketclient.enviar(mensajeCifrado1)
socketclient.enviar(MAC_1)

# Intercambio de información NUMERO 2. Al utilizar K1, reutilizo el canal de comunicaciones aes_cifrado
mensaje2 = ["Hola Amigas"]
jStr_2 = json.dumps(mensaje2)
mensajeCifrado2 = funciones_aes.cifrarAES_CTR(aes, jStr_2.encode("utf-8"))

# Aplico HMAC
hmac_2 = HMAC.new(K2, digestmod=SHA256)
hmac_2.update(mensajeCifrado2)
MAC_2 = hmac_2.digest()

# Envío el json cifrado junto con el nonce del AES CTR, y el mac del HMAC
socketclient.enviar(mensajeCifrado2)
socketclient.enviar(MAC_2)

# Cierro el socket
socketclient.cerrar()