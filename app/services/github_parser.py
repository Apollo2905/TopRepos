import requests
from app.db.connection import get_db_connection

def fetch_top_repos():
    response = requests.get("https://api.github.com/search/repositories", params={"q": "stars:>1", "sort": "stars", "order": "desc"})
    response.raise_for_status()
    data = response.json()
    return data["items"]

def update_top_repos():
    repos = fetch_top_repos()
    with get_db_connection() as db:
        with db.cursor() as cursor:
            for idx, repo in enumerate(repos[:100]):
                cursor.execute("""
                INSERT INTO top100 (repo, owner, position_cur, stars, watchers, forks, open_issues, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (repo) DO UPDATE SET 
                    position_cur = %s,
                    stars = %s,
                    watchers = %s,
                    forks = %s,
                    open_issues = %s,
                    language = %s
                """, (
                    repo["full_name"], repo["owner"]["login"], idx + 1,
                    repo["stargazers_count"], repo["watchers_count"], repo["forks_count"],
                    repo["open_issues_count"], repo["language"],
                    idx + 1, repo["stargazers_count"], repo["watchers_count"],
                    repo["forks_count"], repo["open_issues_count"], repo["language"]
                ))