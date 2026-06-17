# Etapa 1: Construcción (Usamos Maven con Java 17)
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copiamos el pom.xml y el código fuente
COPY pom.xml .
COPY src ./src

# Compilamos el proyecto omitiendo los tests para que sea más rápido
RUN mvn clean package -DskipTests

# Etapa 2: Ejecución (Usamos una imagen más ligera solo con Java)
FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app

# COPIAMOS EL .WAR DESDE LA ETAPA DE CONSTRUCCIÓN
COPY --from=build /app/target/*.war app.war

# Exponemos el puerto
EXPOSE 8080

# Ejecutamos el archivo
ENTRYPOINT ["java", "-jar", "app.war"]