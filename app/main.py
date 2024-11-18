from decimal import Decimal
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

from app.models import UseageReport, UseageItem, CopilotMessages
from app.utils import get_copilot_messages, calculate_message_cost, add_report_details_for_messages

app = FastAPI()


@app.get("/tech-task/usage/")
async def get_useage_report():
    copilot_messages = await get_copilot_messages()
    # Hydrate messages with report costs and names
    hydrated_messages = await add_report_details_for_messages(copilot_messages)

    useage_items = []

    for message in hydrated_messages.messages:
        # If we don't have a report cost then calculate it
        if not message.cost:
            message.cost = calculate_message_cost(message=message.text)

        useage_item = UseageItem(message_id=message.id,
                                 timestamp=message.timestamp,
                                 credits_used=message.cost
                                 )

        useage_items.append(useage_item)

    return UseageReport(useage=useage_items)
