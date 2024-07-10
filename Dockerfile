# Dockerfile for Flask app
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5500
CMD ["gunicorn", "--bind", ":5500", "app:app"]
