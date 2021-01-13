FROM python:3.7

RUN apt-get update

RUN apt-get install -y git

RUN git clone https://github.com/mhenrichsen/ps5-stock.git

WORKDIR /ps5-stock

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "main.py", "&", "python", "scraper.py"]