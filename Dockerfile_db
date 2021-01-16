FROM python:3.7

RUN pip install uvicorn fastapi aiofiles

WORKDIR /app

COPY database.py /app

COPY sql.db /app

CMD ["python", "database.py"]