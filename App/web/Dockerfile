FROM python:3.9.20-slim-bookworm

RUN apt-get -y update; apt-get -y install curl

WORKDIR /web 
COPY requirements.txt /web
RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000
COPY . /web 

ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
