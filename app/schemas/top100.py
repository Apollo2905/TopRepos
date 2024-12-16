from pydantic import BaseModel
from typing import Optional


class RepoBase(BaseModel):
    repo: str  # Название репозитория (full_name в GitHub API)
    owner: str  # Владелец репозитория
    stars: int  # Количество звёзд
    watchers: int  # Количество просмотров
    forks: int  # Количество форков
    open_issues: int  # Количество открытых issues
    language: Optional[str]  # Язык программирования (может быть None)


class RepoInDB(RepoBase):
    position_cur: int  # Текущая позиция в топе
    position_prev: Optional[int]  # Предыдущая позиция в топе


class RepoResponse(RepoInDB):
    pass  # Для ответа API (можно добавить дополнительные поля, если нужно)