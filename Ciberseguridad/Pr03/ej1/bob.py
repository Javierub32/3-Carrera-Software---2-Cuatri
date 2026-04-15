import rsa_funciones

pk_bob = rsa_funciones.cargar_RSAKey_Privada("./Ciberseguridad/Pr03/ej1/bob_private.pem", "password_bob")
pub_alice = rsa_funciones.cargar_RSAKey_Publica("./Ciberseguridad/Pr03/ej1/alice_public.pub")

texto_cifrado = open("./Ciberseguridad/Pr03/ej1/cifrado.bin", "rb").read()
firma = open("./Ciberseguridad/Pr03/ej1/firmado.bin", "rb").read()

texto_descifrado = rsa_funciones.descifrarRSA_OAEP(texto_cifrado, pk_bob)
firma = rsa_funciones.comprobarRSA_PSS("Hola amigos de la seguridad", firma, pub_alice)

print(texto_descifrado)
print(firma)
