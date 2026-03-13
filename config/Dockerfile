FROM python:3.12-slim

# Set environment variables to keep Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Django runs on
EXPOSE 8000

# The corrected JSON/Exec form
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]