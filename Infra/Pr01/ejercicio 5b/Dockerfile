# ETAPA 1: Construcción (Builder)
# Usamos la imagen tiene Maven y el JDK (más pesada, pero necesaria para compilar)
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

COPY pom.xml .

# Descargamos las dependencias sin compilar el proyecto, para aprovechar la caché de Docker
# Si cambiamos el código pero no el pom.xml, Docker usará la caché de esta capa y no descargá de dependencias
RUN mvn dependency:go-offline

COPY src ./src

# Compilamos el proyecto, generando el .jar en la carpeta target/
RUN mvn clean package -DskipTests


# ETAPA 2: Ejecución (Runtime)
# Usamos una imagen que SOLO tiene el JRE (más ligera, pero no sirve para compilar)
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copiamos SOLO el archivo .jar desde la etapa anterior ("builder")
COPY --from=builder /app/target/*.jar app.jar

# Exponemos el puerto
EXPOSE 8080

# Comando para arrancar la aplicación
CMD ["java", "-jar", "app.jar"]