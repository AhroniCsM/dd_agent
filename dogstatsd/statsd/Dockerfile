FROM python:3.9-slim

# Set environment variables

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["opentelemetry-instrument","python", "dogstatsd.py"]
