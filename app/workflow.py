import logging
import time

from app.models import AutomationEvent
from app.storage import is_event_processed, mark_event_processed


logger = logging.getLogger(__name__)




def perform_processing(event: AutomationEvent):
    return {
        "status": "processed",
        "event_id": event.event_id,
        "event_type": event.event_type,
    }


def process_event(event: AutomationEvent):
    if is_event_processed(event.event_id):
        return {
            "status": "duplicate", 
            "event_id": event.event_id,
        }

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(
                "Processing event %s, attempt %s/%s",
                event.event_id,
                attempt,
                max_attempts,
            )

            result = perform_processing(event)

            mark_event_processed(event.event_id)

            logger.info(
                "Event %s processed successfully",
                event.event_id,
            )

            return result

        
        except RuntimeError as exc:
            logger.warning(
                "Event %s failed on attempt %s/%s: %s",
                event.event_id,
                attempt,
                max_attempts,
                exc,
            )


            if attempt == max_attempts:
                logger.error(
                    "Event %s failed after %s attempts",
                    event.event_id,
                    max_attempts,
                )
                raise

            time.sleep(attempt)



