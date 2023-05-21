FROM python:3.10
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod +x /app/worker-entrypoint.sh
RUN chmod +x /app/beat-entrypoint.sh
