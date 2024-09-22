FROM python:3.9.20-slim-bookworm

WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app

ENTRYPOINT ["python3"]
CMD ["/app/app.py"]