FROM python:3.11-slim

WORKDIR /ai-engine

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "health_report.py"]
