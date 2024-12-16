from pydantic import BaseModel
from typing import List
from datetime import date


class ActivityRecord(BaseModel):
    date: date  # Дата активности
    commits: int  # Количество коммитов за день
    authors: List[str]  # Список авторов коммитов


class ActivityResponse(BaseModel):
    repo: str  # Название репозитория (для контекста)
    owner: str  # Владелец репозитория
    activity: List[ActivityRecord]  # Список записей об активности