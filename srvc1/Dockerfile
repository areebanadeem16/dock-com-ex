FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN chmod +x /app/docker-stop.sh
RUN pip install flask requests docker flask_cors
EXPOSE 8199
CMD ["python", "app.py"]
