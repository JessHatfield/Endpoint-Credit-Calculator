import asyncio
from decimal import Decimal

import httpx
from fastapi import HTTPException

from app.models import CopilotMessages, CopilotMessage, HydratedCopilotMessages, HydratedCopilotMessage

API_URL = 'https://owpublic.blob.core.windows.net'


async def get_copilot_messages() -> CopilotMessages:
    try:
        response = httpx.get(f'{API_URL}/tech-task/messages/current-period')
        response.raise_for_status()

        data = response.json()

        copilot_messages = []
        for message in data['messages']:
            copilot_messages.append(
                CopilotMessage(text=message['text'], timestamp=message['timestamp'], id=message['id'],
                               report_id=message.get('report_id', None)))

        return CopilotMessages(messages=copilot_messages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_report_details_for_messages(messages: CopilotMessages) -> HydratedCopilotMessages:
    async def make_request(client: httpx.AsyncClient, copilot_message: CopilotMessage) -> HydratedCopilotMessage:

        cost = None
        report_name = None

        # If a report exists then we try and retrieve its cost
        if copilot_message.report_id:
            url = f"{API_URL}/tech-task/reports/{copilot_message.report_id}"
            response = await client.get(url)

            if response.status_code == 404:
                # If we can't find a report then don't set credit cost or report name
                return HydratedCopilotMessage(text=copilot_message.text, timestamp=copilot_message.timestamp,
                                              id=copilot_message.id, report_id=copilot_message.report_id)

            response.raise_for_status()
            data = response.json()
            cost = Decimal(f'{round(data['credit_cost'], 2)}')
            report_name = data['name']

        return HydratedCopilotMessage(text=copilot_message.text,
                                      timestamp=copilot_message.timestamp,
                                      id=copilot_message.id,
                                      report_id=copilot_message.report_id,
                                      report_name=report_name,
                                      cost=cost)

    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, copilot_message) for copilot_message in messages.messages]
        results = await asyncio.gather(*tasks)

        return HydratedCopilotMessages(messages=results)


def calculate_message_cost(message: CopilotMessage) -> Decimal:
    pass
