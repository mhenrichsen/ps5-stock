FROM python:3.7

COPY . /app

WORKDIR /app

RUN apt-get update

RUN apt-get install -y git

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "main.py"]