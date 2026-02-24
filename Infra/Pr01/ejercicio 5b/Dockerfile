# ==========================================
# ETAPA 1: Construcción (Builder)
# ==========================================
# Usamos la imagen pesada que tiene Maven y el JDK
FROM maven:3.9-eclipse-temurin-17 AS builder

# Definimos el directorio de trabajo
WORKDIR /app

# Descargamos dependencias (aprovechando la caché)
COPY pom.xml .
RUN mvn dependency:go-offline

# Copiamos el código y compilamos el .jar
COPY src ./src
RUN mvn clean package -DskipTests

# ==========================================
# ETAPA 2: Ejecución (Runtime)
# ==========================================
# Usamos una imagen ultra-ligera (Alpine Linux) que SOLO tiene el JRE (Java Runtime Environment)
FROM eclipse-temurin:17-jre-alpine

# Directorio de trabajo en la nueva imagen limpia
WORKDIR /app

# Copiamos SOLO el archivo .jar desde la etapa anterior ("builder")
# y lo renombramos a "app.jar" para que sea más fácil de ejecutar
COPY --from=builder /app/target/*.jar app.jar

# Exponemos el puerto
EXPOSE 8080

# Comando para arrancar la aplicación
CMD ["java", "-jar", "app.jar"]