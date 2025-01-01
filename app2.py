import time
import logging
from ddtrace import tracer, patch_all

# Automatically patch all supported libraries
patch_all()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def do_work():
    logger.info("Starting do_work")
    with tracer.trace("do_work") as span:
        span.set_tag("work_type", "example")
        logger.info("Work type set to 'example'")
        # Additional span within do_work
        with tracer.trace("do_work.step1") as step_span:
            step_span.set_tag("step", "1")
            logger.info("Executing step 1 of do_work")
            time.sleep(0.5)  # Simulate step 1 work
            logger.info("Completed step 1 of do_work")
        with tracer.trace("do_work.step2") as step_span:
            step_span.set_tag("step", "2")
            logger.info("Executing step 2 of do_work")
            time.sleep(0.5)  # Simulate step 2 work
            logger.info("Completed step 2 of do_work")
    logger.info("Completed do_work")

def main():
    logger.info("Starting main execution")
    with tracer.trace("main") as span:
        span.set_tag("operation", "main_execution")
        logger.info("Main operation set to 'main_execution'")
        do_work()
        # Additional span within main
        with tracer.trace("main.additional_work") as additional_span:
            additional_span.set_tag("additional_task", "true")
            logger.info("Executing additional task in main")
            time.sleep(1)  # Simulate additional work
            logger.info("Completed additional task in main")
    logger.info("Completed main execution")

if __name__ == "__main__":
    while True:
        logger.info("Starting new iteration of the main loop")
        main()
        logger.info("Waiting for the next iteration")
        time.sleep(30)  # Wait for 30 seconds before running the traces again
