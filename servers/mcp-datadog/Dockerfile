FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app
COPY . /app


EXPOSE 8001
CMD ["python", "main.py"]