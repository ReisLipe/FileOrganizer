FROM python:3.9-slim
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ /app/src

CMD ["python", "/app/src/main.py", "--path", "/data"]