FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY services/graph/app ./app
COPY libs /libs
ENV PYTHONPATH="/app:/libs"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
