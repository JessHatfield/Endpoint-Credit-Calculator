from decimal import Decimal

from app.models import CopilotMessages, CopilotMessage, HydratedCopilotMessages


async def get_copilot_messages() -> CopilotMessages:
    pass


async def add_report_details_for_messages(messages: CopilotMessages) -> HydratedCopilotMessages:
    # for message in CopilotMessages:
    #     if message.report_id:
    #         response=requests

    return HydratedCopilotMessages()


def calculate_message_cost(message: CopilotMessage) -> Decimal:
    pass
