from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter

# Ejercicio 1

# Datos necesarios
key = get_random_bytes(8) # Clave aleatoria de 64 bits
IV = get_random_bytes(8)  # IV aleatorio de 64 bits
BLOCK_SIZE_DES = 8 # Bloque de 64 bits

key_aes = get_random_bytes(16) # Clave aleatoria de 128 bits
IV_aes = get_random_bytes(16)  # IV aleatorio de 128 bits
BLOCK_SIZE_AES = 16 # Bloque de 128 bits


def cifradoDes(data, key, IV, BLOCK_SIZE_DES):
	# Creamos un mecanismo de cifrado DES en modo CBC con un vector de inicialización IV
	cipher = DES.new(key, DES.MODE_CBC, IV)

	# Ciframos, haciendo que la variable “data” sea múltiplo del tamaño de bloque
	ciphertext = cipher.encrypt(pad(data,BLOCK_SIZE_DES))
 
	return ciphertext

def desCifradoDes(data, key, IV, BLOCK_SIZE_DES):
	# Creamos un mecanismo de cifrado DES en modo CBC con un vector de inicialización IV
	desCipher = DES.new(key, DES.MODE_CBC, IV)

	# Desciframos, eliminamos el padding, y recuperamos la cadena
	original = unpad(desCipher.decrypt(data), BLOCK_SIZE_DES).decode("utf-8", "ignore")
 
	return original

def cifradoAes(data, key, IV, BLOCK_SIZE_AES):
	# Creamos un mecanismo de cifrado AES en modo CBC con un vector de inicialización IV
	cipher = AES.new(key, AES.MODE_CBC, IV)

	# Ciframos, haciendo que la variable “data” sea múltiplo del tamaño de bloque
	ciphertext = cipher.encrypt(pad(data,BLOCK_SIZE_AES))
 
	return ciphertext

def desCifradoAes(data, key, IV, BLOCK_SIZE_AES):
	# Creamos un mecanismo de cifrado AES en modo CBC con un vector de inicialización IV
	desCipher = AES.new(key, AES.MODE_CBC, IV)

	# Desciframos, eliminamos el padding, y recuperamos la cadena
	original = unpad(desCipher.decrypt(data), BLOCK_SIZE_AES).decode("utf-8", "ignore")
 
	return original

data = "Hola amigas de la seguridad".encode("utf-8") # Datos a cifrar
data2 = "Hola amigos de la seguridad".encode("utf-8")
    

print("Datos originales:", data.decode("utf-8", "ignore"))
print("Cifrado DES:", cifradoDes(data, key, IV, BLOCK_SIZE_DES).hex())
print("Descifrado DES:", desCifradoDes(cifradoDes(data, key, IV, BLOCK_SIZE_DES), key, IV, BLOCK_SIZE_DES))

print("\n")

print("Datos originales:", data2.decode("utf-8", "ignore"))
print("Cifrado DES:", cifradoDes(data2, key, IV, BLOCK_SIZE_DES).hex())
print("Descifrado DES:", desCifradoDes(cifradoDes(data2, key, IV, BLOCK_SIZE_DES), key, IV, BLOCK_SIZE_DES))

print("\n")

print("Datos originales:", data.decode("utf-8", "ignore"))
print("Cifrado AES:", cifradoAes(data, key_aes, IV_aes, BLOCK_SIZE_AES).hex())
print("Descifrado AES:", desCifradoAes(cifradoAes(data, key_aes, IV_aes, BLOCK_SIZE_AES), key_aes, IV_aes, BLOCK_SIZE_AES))


# Ejercicio 2
def cifradoAesCustom(data, key, mode):
	"""Cifra datos usando AES con diferentes modos de operación"""

	# ECB no requiere IV
	if mode == "ECB":
		cipher = AES.new(key, AES.MODE_ECB)
		ciphertext = cipher.encrypt(pad(data, AES.block_size))
		return ciphertext, None, None
	
	# CTR requiere nonce (tamaño de bloque / 2 = 8 bytes)
	elif mode == "CTR":
		nonce = get_random_bytes(AES.block_size//2)
		cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
		ciphertext = cipher.encrypt(data)  # CTR no requiere padding
		return ciphertext, nonce, None
	
	# OFB requiere IV aleatorio
	elif mode == "OFB":
		iv = get_random_bytes(AES.block_size)
		cipher = AES.new(key, AES.MODE_OFB, iv=iv)
		ciphertext = cipher.encrypt(data)  # OFB no requiere padding
		return ciphertext, iv, None
	
	# CFB requiere IV aleatorio
	elif mode == "CFB":
		iv = get_random_bytes(AES.block_size)
		cipher = AES.new(key, AES.MODE_CFB, iv=iv)
		ciphertext = cipher.encrypt(data)  # CFB no requiere padding
		return ciphertext, iv, None

	# GCM requiere nonce (tamaño de bloque = 16 bytes) y mac_len
	elif mode == "GCM":
		nonce = get_random_bytes(AES.block_size)
		cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16)
		ciphertext, tag = cipher.encrypt_and_digest(data)  # GCM no requiere padding
		return ciphertext, nonce, tag
	
	else:
		return None, None, None

def desCifradoAesCustom(ciphertext, key, mode, param, tag=None):
	"""Descifra datos usando AES con diferentes modos de operación"""
	
	if mode == "ECB":
		# ECB no requiere IV
		cipher = AES.new(key, AES.MODE_ECB)
		plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
		return plaintext.decode("utf-8", "ignore")
	
	elif mode == "CTR":
		# CTR requiere el mismo nonce usado en el cifrado
		cipher = AES.new(key, AES.MODE_CTR, nonce=param)
		plaintext = cipher.decrypt(ciphertext)
		return plaintext.decode("utf-8", "ignore")
	
	elif mode == "OFB":
		# OFB requiere el mismo IV usado en el cifrado
		cipher = AES.new(key, AES.MODE_OFB, iv=param)
		plaintext = cipher.decrypt(ciphertext)
		return plaintext.decode("utf-8", "ignore")
	
	elif mode == "CFB":
		# CFB requiere el mismo IV usado en el cifrado
		cipher = AES.new(key, AES.MODE_CFB, iv=param)
		plaintext = cipher.decrypt(ciphertext)
		return plaintext.decode("utf-8", "ignore")
	
	elif mode == "GCM":
		# GCM requiere el nonce y el tag para verificar autenticidad
		cipher = AES.new(key, AES.MODE_GCM, nonce=param, mac_len=16)
		plaintext = cipher.decrypt_and_verify(ciphertext, tag)
		return plaintext.decode("utf-8", "ignore")
	
	else:
		return None

# Probar todos los modos
print("EJERCICIO 2: Cifrado AES con diferentes modos de operación")

mensaje = "Hola Amigos de Seguridad".encode("utf-8")
print(f"\nMensaje original: {mensaje.decode('utf-8')}\n")

modos = ["ECB", "CTR", "OFB", "CFB", "GCM"]

for modo in modos:
	print(f"--- Modo {modo} ---")
	ciphertext, param, tag = cifradoAesCustom(mensaje, key_aes, modo)
	print(f"Cifrado: {ciphertext.hex()}")
	
	descifrado = desCifradoAesCustom(ciphertext, key_aes, modo, param, tag)
	print(f"Descifrado: {descifrado}")
	print()