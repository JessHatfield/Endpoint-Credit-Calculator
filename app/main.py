from decimal import Decimal
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

from app.models import UseageReport, UseageItem, CopilotMessages
from app.utils import get_copilot_messages

app = FastAPI()


@app.get("/tech-task/usage/")
async def get_useage_report(context: CopilotMessages = Depends(get_copilot_messages)):
    useage_items = []

    for message in context:
        useage_items.append(UseageItem())

    return UseageReport(useage=useage_items)
