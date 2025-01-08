import os
import time
import logging
from datadog.dogstatsd import DogStatsd
from ddtrace import tracer, patch_all

# Enable auto-instrumentation
patch_all()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# StatsD Configuration
STATSD_HOST = os.getenv("STATSD_HOST", "127.0.0.1")
STATSD_PORT = int(os.getenv("STATSD_PORT", 8128))  # Match OpenTelemetry configuration
statsd_client = DogStatsd(host=STATSD_HOST, port=STATSD_PORT)

# Metric Names
INTERFACE_METRIC = "app.interface.metric"
INGESTED_METRIC = "app.ingested.metric"

# Reusable Functions for Metrics
def increment_statsd_counter(metric_name, metric_value, app_token):
    statsd_client.increment(metric_name, metric_value, tags=[f"app_token:{app_token}"])
    logger.info(f"Incremented counter metric: {metric_name} with value: {metric_value}")

def send_statsd_gauge(metric_name, metric_value, app_token):
    statsd_client.gauge(metric_name, metric_value, tags=[f"app_token:{app_token}"])
    logger.info(f"Sent gauge metric: {metric_name} with value: {metric_value}")

# Application Logic
def do_work(app_token):
    logger.info("Starting do_work")

    # Increment interface metric
    with tracer.trace("do_work") as span:
        span.set_tag("work_type", "example")
        logger.info("Work type set to 'example'")
        increment_statsd_counter(INTERFACE_METRIC, 1, app_token)
        logger.info("Incremented interface metric")

    # Simulated steps
    with tracer.trace("do_work.step1") as step_span:
        step_span.set_tag("step", "1")
        logger.info("Executing step 1 of do_work")
        time.sleep(0.5)
        logger.info("Completed step 1 of do_work")
    with tracer.trace("do_work.step2") as step_span:
        step_span.set_tag("step", "2")
        logger.info("Executing step 2 of do_work")
        time.sleep(0.5)
        logger.info("Completed step 2 of do_work")
        send_statsd_gauge(INGESTED_METRIC, 42, app_token)
        logger.info("Set ingested metric gauge to 42")

    logger.info("Completed do_work")

def main():
    app_token = "your_app_token"  # Replace with your actual app token
    logger.info("Starting main execution")
    with tracer.trace("main") as span:
        span.set_tag("operation", "main_execution")
        logger.info("Main operation set to 'main_execution'")
        do_work(app_token)

        # Additional work
        with tracer.trace("main.additional_work") as additional_span:
            additional_span.set_tag("additional_task", "true")
            logger.info("Executing additional task in main")
            time.sleep(1)
            logger.info("Completed additional task in main")
            increment_statsd_counter(INTERFACE_METRIC, 1, app_token)
            logger.info("Incremented interface metric for additional task")

    logger.info("Completed main execution")

if __name__ == "__main__":
    while True:
        logger.info("Starting new iteration of the main loop")
        main()
        logger.info("Waiting for the next iteration")
        time.sleep(30)  # Wait for 30 seconds before the next run
