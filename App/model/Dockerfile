FROM python:3.9.20-slim-bookworm

WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app

CMD ["fastapi", "run", "/app/app.py", "--port", "5555"]