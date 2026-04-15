import rsa_funciones

# Creamos y guardamos las claves de Alice
print(" Generando claves de Alice...")
alice_key = rsa_funciones.crear_RSAKey()
rsa_funciones.guardar_RSAKey_Privada("./Ciberseguridad/Pr03/ej1/alice_private.pem", alice_key, "password_alice")
rsa_funciones.guardar_RSAKey_Publica("./Ciberseguridad/Pr03/ej1/alice_public.pub", alice_key)

# Creamos y guardamos las claves de Bob
print(" Generando claves de Bob...")
bob_key = rsa_funciones.crear_RSAKey()
rsa_funciones.guardar_RSAKey_Privada("./Ciberseguridad/Pr03/ej1/bob_private.pem", bob_key, "password_bob")
rsa_funciones.guardar_RSAKey_Publica("./Ciberseguridad/Pr03/ej1/bob_public.pub", bob_key)
