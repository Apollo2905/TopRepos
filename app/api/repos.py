from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
from schemas.top100 import RepoResponse
from schemas.activity import ActivityResponse
from db.connection import get_db_connection

router = APIRouter()

# GET /api/repos/top100
@router.get("/api/repos/top100", response_model=List[RepoResponse])
async def get_top_100_repos(
    sort_by: Optional[str] = Query(None, description="Поле для сортировки"),
    order: Optional[str] = Query("desc", description="Порядок сортировки: asc или desc"),
    db=Depends(get_db_connection)
):
    """
    Возвращает топ-100 публичных репозиториев из таблицы top100, с опциональной сортировкой.
    """
    valid_sort_fields = ["stars", "watchers", "forks", "open_issues", "position_cur", "position_prev"]
    
    # Валидация параметра sort_by
    if sort_by and sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
    
    # Построение SQL-запроса
    sort_clause = f"ORDER BY {sort_by} {order.upper()}" if sort_by else "ORDER BY stars DESC"
    query = f"""
        SELECT repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        FROM top100
        {sort_clause}
        LIMIT 100;
    """
    async with db.acquire() as conn:
        result = await conn.fetch(query)
        return [dict(record) for record in result]


# GET /api/repos/{owner}/{repo}/activity
@router.get("/api/repos/{owner}/{repo}/activity", response_model=ActivityResponse)
async def get_repo_activity(
    owner: str,
    repo: str,
    since: date = Query(..., description="Дата начала периода"),
    until: date = Query(..., description="Дата конца периода"),
    db=Depends(get_db_connection)
):
    """
    Возвращает информацию об активности репозитория за указанный период (помесячно).
    """
    # Проверка корректности периода
    if since > until:
        raise HTTPException(status_code=400, detail="since must be before or equal to until")
    
    # SQL-запрос
    query = f"""
        SELECT date, commits, authors
        FROM activity
        WHERE repo = $1 AND owner = $2 AND date BETWEEN $3 AND $4
        ORDER BY date ASC;
    """
    async with db.acquire() as conn:
        result = await conn.fetch(query, repo, owner, since, until)
        if not result:
            raise HTTPException(status_code=404, detail="No activity found for the given repository and period")
        
        activity = [dict(record) for record in result]
        return {"repo": repo, "owner": owner, "activity": activity}