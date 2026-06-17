FROM webapp-base:latest

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 5000

CMD ["flask", "run",  "--host=0.0.0.0",  "--port=5000"]