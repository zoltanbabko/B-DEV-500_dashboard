##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## github.py
##

import httpx
from fastapi import HTTPException
from app.services.registry import register_widget

@register_widget(
    service="github",
    name="User Profile",
    type="user_profile",
    description="Display GitHub user profile information.",
    params=[]
)
async def get_github_profile(params: dict, token: str):
    if not token:
        raise HTTPException(status_code=401, detail="GitHub is not connected")

    headers = {
        "Authorization": f"Bearer {token}", 
        "Accept": "application/vnd.github.v3+json"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.github.com/user", headers=headers)

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Error API GitHub try to reconnect GitHub")

        data = resp.json()

        return {
            "username": data.get("login"),
            "avatar": data.get("avatar_url"),
            "repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "bio": data.get("bio")
        }

@register_widget(
    service="github",
    name="GitHub Issues",
    type="github_issues",
    description="Display open issues of a GitHub repository.",
    params=[{"name": "repo", "type": "string", "label": "Repo (ex: user/projet)"}]
)
async def get_github_issues(params: dict, token: str):
    repo = params.get("repo")
    if not repo:
        raise HTTPException(status_code=400, detail="Parameter 'repo' is required")
    if not token:
        raise HTTPException(status_code=401, detail="GitHub is not connected")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.github.com/repos/{repo}/issues", 
            headers=headers, 
            params={"state": "open", "per_page": 5}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=404, detail="Repository not found or access denied")

        issues = resp.json()
        return [
            {
                "title": i["title"],
                "number": i["number"],
                "url": i["html_url"],
                "user": i["user"]["login"]
            } for i in issues
        ]
