FROM python:3.9-slim

WORKDIR /app


RUN mkdir data

COPY config.json data/config.json

# Copiar el código
COPY app.py .

CMD ["python", "app.py"]