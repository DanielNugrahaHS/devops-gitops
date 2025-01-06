FROM python:3.9-slim

RUN pip install pika requests

COPY test_service.py /app/test_service.py

CMD ["python", "/app/test_service.py"]
