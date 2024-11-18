from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class UseageItem(BaseModel):
    message_id: int
    timestamp: str
    report_name: str | None = None
    credits_used: Decimal


class UseageReport(BaseModel):
    useage: List[UseageItem] = Field(default_factory=list)


class CopilotMessage(BaseModel):
    text: str
    timestamp: str
    id: int
    report_id: int | None


class CopilotMessages(BaseModel):
    messages = List[CopilotMessage]
