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
    report_id: int | None = None


class CopilotMessages(BaseModel):
    messages: List[CopilotMessage]


class HydratedCopilotMessage(BaseModel):
    text: str
    timestamp: str
    id: int
    report_id: int | None = None
    cost: Decimal | None = None
    report_name: str | None = None


class HydratedCopilotMessages(BaseModel):
    messages: List[HydratedCopilotMessage]
