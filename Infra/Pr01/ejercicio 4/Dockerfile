# 1. Usamos Node.js versión 18 con la variante "alpine" (una versión de Linux ultraligera)
FROM node:18-alpine

# 2. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos SOLO el package.json primero para aprovechar la caché de Docker
COPY package.json .

# 4. Instalamos las dependencias de Node.js
RUN npm install

# 5. Copiamos el resto del código (el archivo server.js)
COPY server.js .

# 6. Exponemos el puerto 3000, que es donde escucha nuestra app
EXPOSE 3000

# 7. Definimos el comando para arrancar la aplicación
CMD ["npm", "start"]