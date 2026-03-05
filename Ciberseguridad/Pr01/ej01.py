def cifradoCesarAlfabetoInglesMAYConEspacios(cadena, desplazamiento = 3):
    """Devuelve un cifrado Cesar tradicional (+desplazamiento)"""
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        if (ordenClaro >= 65 and ordenClaro <= 90):
            ordenCifrado = (((ordenClaro - 65) + desplazamiento) % 26) + 65
        if (ordenClaro >= 97 and ordenClaro <= 122):
            ordenCifrado = (((ordenClaro - 97) + desplazamiento) % 26) + 97
        if (ordenClaro == 32):
            ordenCifrado = 32
        resultado = resultado + chr(ordenCifrado)
        i = i + 1
    return resultado

def desCifradoCesarAlfabetoInglesMAYConEspacios(cadena, desplazamiento = 3):
	"""Devuelve un descifrado Cesar tradicional (-desplazamiento)"""
	resultado = ''
	i = 0
	while i < len(cadena):
		ordenCifrado = ord(cadena[i])
		ordenClaro = 0
		if (ordenCifrado >= 65 and ordenCifrado <= 90):
			ordenClaro = (((ordenCifrado - 65) - desplazamiento) % 26) + 65
		if (ordenCifrado >= 97 and ordenCifrado <= 122):
			ordenClaro = (((ordenCifrado - 97) - desplazamiento) % 26) + 97
		if (ordenCifrado == 32):
			ordenClaro = 32
		resultado = resultado + chr(ordenClaro)
		i = i + 1
	return resultado

def cifradoCesarAlfabetoInglesMAYSinEspacios(cadena, desplazamiento = 3):
    """Devuelve un cifrado Cesar tradicional (+desplazamiento)"""
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        if (ordenClaro >= 65 and ordenClaro <= 90):
            ordenCifrado = (((ordenClaro - 65) + desplazamiento) % 26) + 65
        if (ordenClaro >= 97 and ordenClaro <= 122):
            ordenCifrado = (((ordenClaro - 97) + desplazamiento) % 26) + 97
        resultado = resultado + chr(ordenCifrado)
        i = i + 1
    return resultado

def desCifradoCesarAlfabetoInglesMAYSinEspacios(cadena, desplazamiento = 3):
	"""Devuelve un descifrado Cesar tradicional (-desplazamiento)"""
	resultado = ''
	i = 0
	while i < len(cadena):
		ordenCifrado = ord(cadena[i])
		ordenClaro = 0
		if (ordenCifrado >= 65 and ordenCifrado <= 90):
			ordenClaro = (((ordenCifrado - 65) - desplazamiento) % 26) + 65
		if (ordenCifrado >= 97 and ordenCifrado <= 122):
			ordenClaro = (((ordenCifrado - 97) - desplazamiento) % 26) + 97
		resultado = resultado + chr(ordenClaro)
		i = i + 1
	return resultado

claroCESARMAY = 'VeNI ViDI VINCi AURIa'
print("Cadena original:", claroCESARMAY)
cifradoCESARMAY = cifradoCesarAlfabetoInglesMAYConEspacios(claroCESARMAY) 
print("Cadena cifrada con desplazamiento 3 y respetando espacios:", cifradoCESARMAY)
descifradoCESARMAY = desCifradoCesarAlfabetoInglesMAYConEspacios(cifradoCESARMAY)
print("Cadena descifrada con desplazamiento 3 y respetando espacios:", descifradoCESARMAY)

cifradoCESARMAY = cifradoCesarAlfabetoInglesMAYConEspacios(claroCESARMAY, 5) 
print("Cadena cifrada con desplazamiento 5 y respetando espacios:", cifradoCESARMAY)
descifradoCESARMAY = desCifradoCesarAlfabetoInglesMAYConEspacios(cifradoCESARMAY, 5)
print("Cadena descifrada con desplazamiento 5 y respetando espacios:", descifradoCESARMAY)

cifradoCESARMAY = cifradoCesarAlfabetoInglesMAYSinEspacios(claroCESARMAY, 5) 
print("Cadena cifrada con desplazamiento 5 y sin respetar espacios:", cifradoCESARMAY)
descifradoCESARMAY = desCifradoCesarAlfabetoInglesMAYSinEspacios(cifradoCESARMAY, 5)
print("Cadena descifrada con desplazamiento 5 y sin respetar espacios:", descifradoCESARMAY)