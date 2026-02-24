# Usamos Node.js versión 18 con la variante "alpine" (una versión de Linux ultraligera)
FROM node:18-alpine

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos SOLO el package.json primero para aprovechar la caché de Docker
COPY package.json .

# Instalamos las dependencias de Node.js
RUN npm install

# Copiamos el resto del código (el archivo server.js)
COPY server.js .

# Exponemos el puerto 3000, que es donde escucha nuestra app
EXPOSE 3000

# Definimos el comando para arrancar la aplicación
CMD ["npm", "start"]