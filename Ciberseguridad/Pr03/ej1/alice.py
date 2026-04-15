import rsa_funciones

pk_alice = rsa_funciones.cargar_RSAKey_Privada("./Ciberseguridad/Pr03/ej1/alice_private.pem", "password_alice")

pub_bob = rsa_funciones.cargar_RSAKey_Publica("./Ciberseguridad/Pr03/ej1/bob_public.pub")

texto = "Hola amigos de la seguridad"

print("Cifrando texto con la clave pública de Bob y firmando con la clave privada de Alice...")
cifrado = rsa_funciones.cifrarRSA_OAEP(texto, pub_bob)
firmado = rsa_funciones.firmarRSA_PSS(texto, pk_alice)

# Guardamos el mensaje cifrado en un fichero binario
file_out = open("./Ciberseguridad/Pr03/ej1/cifrado.bin", "wb")
file_out.write(cifrado)
file_out.close()

# Guardamos la firma en un fichero binario
file_out = open("./Ciberseguridad/Pr03/ej1/firmado.bin", "wb")
file_out.write(firmado)
file_out.close()

print("Archivos guardados.")