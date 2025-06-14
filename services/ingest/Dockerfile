FROM python:3.11-slim
WORKDIR /app

# Install service dependencies
COPY services/ingest/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy service source code and shared libraries
COPY services/ingest /app
COPY libs /libs

# Allow import of shared libs
ENV PYTHONPATH="/app:/libs"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
