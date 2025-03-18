FROM python:3.11

WORKDIR /ranking_engine

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "ranking_engine.py"]
