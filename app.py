from flask import Flask, jsonify
import logging
import random
import time

# Create Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info("Home route accessed")
    return jsonify({"message": "Welcome to the logging app!"})

@app.route('/error')
def error():
    logger.error("Error route accessed")
    return jsonify({"error": "This is an error!"}), 500

# Define an endpoint
@app.route('/generate', methods=['GET'])
def generate_logs_and_traces():
    # Generate a random delay
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)

    # Log a message
    logger.info(f"Processed request with delay: {delay:.2f}s")

    return jsonify({"status": "success", "delay": delay})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)