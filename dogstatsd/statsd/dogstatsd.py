from flask import Flask, jsonify
import logging
import random
import time
import os
from statsd import StatsClient
from threading import Thread

# Create Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure StatsD
statsd_client = StatsClient(
    host=os.getenv("NODE", "localhost"),
    port=int(os.getenv("STATSD_PORT", 8128)),
    prefix='flask_app'
)

# Initialize custom metrics
INGESTED_METRIC = 'ingested'
AHARONESTED_METRIC = 'aharonested'
ALWAYS_METRIC = 'always'

@app.route('/')
def home():
    logger.info("Home route accessed")
    statsd_client.incr(f"{INGESTED_METRIC}_count")  # Increment 'ingested' counter
    return jsonify({"message": "Welcome to the logging app!"})

@app.route('/error')
def error():
    logger.error("Error route accessed")
    statsd_client.incr(f"{AHARONESTED_METRIC}_count")  # Increment 'aharonested' counter
    return jsonify({"error": "This is an error!"}), 500

@app.route('/generate', methods=['GET'])
def generate_logs_and_traces():
    # Generate a random delay
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)

    # Log a message
    logger.info(f"Processed request with delay: {delay:.2f}s")

    # Report delay as a gauge metric
    statsd_client.gauge(f"{INGESTED_METRIC}_delay", delay)

    # Increment 'aharonested' counter if delay > 1.0s
    if delay > 1.0:
        statsd_client.incr(f"{AHARONESTED_METRIC}_slow_request_count")

    return jsonify({"status": "success", "delay": delay})

def increment_always():
    """Background function to increment 'always' metric every 5 seconds."""
    while True:
        statsd_client.incr(f"{ALWAYS_METRIC}_count")
        logger.info(f"Incremented '{ALWAYS_METRIC}_count'")
        time.sleep(5)

if __name__ == '__main__':
    # Start the background thread
    Thread(target=increment_always, daemon=True).start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5600)
