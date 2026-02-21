from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

def test_aes_encryption():
    """Prueba de cifrado AES"""
    print("=== Prueba de cifrado AES ===")
    
    # Generar clave aleatoria de 256 bits
    key = get_random_bytes(32)
    print(f"Clave generada: {key.hex()}")
    
    # Mensaje a cifrar
    mensaje = b"Hola, esto es una prueba de PyCryptodome!"
    print(f"Mensaje original: {mensaje.decode()}")
    
    # Crear cifrador AES en modo CBC
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Cifrar el mensaje (con padding)
    mensaje_cifrado = cipher.encrypt(pad(mensaje, AES.block_size))
    iv = cipher.iv
    
    print(f"Mensaje cifrado: {mensaje_cifrado.hex()}")
    print(f"IV: {iv.hex()}")
    
    # Descifrar
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    mensaje_descifrado = unpad(decipher.decrypt(mensaje_cifrado), AES.block_size)
    
    print(f"Mensaje descifrado: {mensaje_descifrado.decode()}")
    print(f"¿Coincide? {mensaje == mensaje_descifrado}\n")

def test_hash():
    """Prueba de hash SHA256"""
    print("=== Prueba de hash SHA256 ===")
    
    mensaje = b"Este es un mensaje de prueba"
    print(f"Mensaje: {mensaje.decode()}")
    
    # Crear hash
    hash_obj = SHA256.new(mensaje)
    hash_hex = hash_obj.hexdigest()
    
    print(f"Hash SHA256: {hash_hex}")
    print(f"Longitud: {len(hash_hex)} caracteres hexadecimales\n")

def main():
    print("Probando PyCryptodome...\n")
    
    try:
        test_aes_encryption()
        test_hash()
        print("✓ Todas las pruebas completadas exitosamente!")
        print("✓ PyCryptodome está funcionando correctamente!")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
