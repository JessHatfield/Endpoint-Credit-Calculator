import logging

from fastapi import FastAPI
from app.models import UsageReport, UsageItem
from app.utils import get_copilot_messages, calculate_message_cost, add_report_details_for_messages

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


@app.get("/tech-task/usage/")
async def get_usage_report():
    copilot_messages = await get_copilot_messages()
    # Hydrate messages with report costs and names
    hydrated_messages = await add_report_details_for_messages(copilot_messages)

    useage_items = []

    for message in hydrated_messages.messages:
        # If we don't have a report cost then calculate it
        if not message.cost:
            message.cost = calculate_message_cost(message=message)

        usage_item = UsageItem(message_id=message.id,
                                 timestamp=message.timestamp,
                                 credits_used=message.cost
                                 )

        if message.report_name:
            usage_item.report_name = message.report_name

        useage_items.append(usage_item)
    # We have to call model_dump here to remove nested report_name fields where value is none
    # There is probably a neater way of doing this, this was the quickest solution I could find
    return UsageReport(usage=useage_items).model_dump(exclude_none=True)
