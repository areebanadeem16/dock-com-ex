FROM python:3.8-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    procps \
    docker.io \
    bash \
    && apt-get clean

RUN chmod +x /app/docker-stop.sh
RUN pip install flask requests flask_cors psutil docker
EXPOSE 8199
CMD ["python", "app.py"]
