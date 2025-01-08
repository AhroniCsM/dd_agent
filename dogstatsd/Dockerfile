FROM python:3.9-slim

# Set environment variables
ENV DD_ENV="production" \
    DD_SERVICE="python-app-2" \
    DD_VERSION="1.0.0" \
    DD_TRACE_ENABLED=true

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["python", "dogstatsd.py"]
