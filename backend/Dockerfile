FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# Use pip config to increase timeout and retry limit
RUN pip install --no-cache-dir --timeout=600 --retries=10 -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]