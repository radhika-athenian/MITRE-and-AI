FROM python:3.11-slim
WORKDIR /app

# Install service dependencies
COPY services/graph/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy service source and shared libraries
COPY services/graph /app
COPY libs /libs

# Set PYTHONPATH so the service can import shared libraries
ENV PYTHONPATH="/app:/libs"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
