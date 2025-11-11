from django.conf import settings
from .models import ClockifyWorkspace, ClockifyUsers, ClockifyProjects, ClockifyTimeEntry
from django.utils.dateparse import parse_datetime
import requests
import logging

logger = logging.getLogger(__name__)

CLOCKIFY_API_BASE = "https://api.clockify.me/api/v1"

def sync_clockify_workspaces():
    """
    Fetch workspaces from Clockify API and save/update them in the database.
    Returns a list of ClockifyWorkspace objects.
    """
    api_key = settings.CLOCKIFY_API_KEY
    if not api_key:
        return {"error": "Clockify API key is not configured in settings."}

    headers = {"X-Api-Key": api_key}
    url = f"{CLOCKIFY_API_BASE}/workspaces"
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        logger.error("Clockify workspaces request failed: %s", e)
        return {"error": "Request to Clockify failed", "detail": str(e)}

    if response.status_code != 200:
        logger.error("Clockify workspaces fetch failed: %s %s", response.status_code, response.text)
        return {"error": "Failed to fetch workspaces", "status_code": response.status_code, "body": response.text}

    workspaces = response.json()
    saved_workspaces = []

    for ws in workspaces:
        cw_id = ws.get("id")      # Clockify's workspace id (string)
        name = ws.get("name") or ""
        if not cw_id or not name:
            continue
        obj, created = ClockifyWorkspace.objects.update_or_create(
            workspace_id=cw_id,
            defaults={"name": name}
        )
        saved_workspaces.append(obj)

    return saved_workspaces

def sync_clockify_users():
    """
    Fetch users for all workspaces from Clockify API and save/update them in the database.
    Returns a list of ClockifyUser objects.
    """
    api_key = settings.CLOCKIFY_API_KEY
    if not api_key:
        return {"error": "Clockify API key is not configured in settings."}

    headers = {"X-Api-Key": api_key}
    all_users = []

    workspaces = ClockifyWorkspace.objects.all()
    if not workspaces.exists():
        return {"error": "No workspaces found. Please sync workspaces first."}

    for workspace in workspaces:
        url = f"{CLOCKIFY_API_BASE}/workspaces/{workspace.workspace_id}/users"

        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.RequestException as e:
            logger.error(f"Clockify users request failed for workspace {workspace.name}: %s", e)
            continue

        if response.status_code != 200:
            logger.error("Clockify users fetch failed for %s: %s %s", workspace.name, response.status_code, response.text)
            continue

        users = response.json()
        for user in users:
            u_id = user.get("id")
            name = user.get("name") or ""
            email = user.get("email") or ""

            if not u_id or not email:
                continue

            obj, _ = ClockifyUsers.objects.update_or_create(
                user_id=u_id,
                defaults={
                    "name": name,
                    "email": email,
                    "workspace": workspace
                }
            )
            all_users.append(obj)

    return all_users

def sync_clockify_projects():
    """
    Fetch projects from Clockify API for each workspace and save them in the database.
    Returns a list of all saved Projects objects.
    """
    api_key = settings.CLOCKIFY_API_KEY
    if not api_key:
        return {"error": "Clockify API key is not configured in settings."}

    headers = {"X-Api-Key": api_key}
    saved_projects = []

    # Loop through all workspaces in your database
    for workspace in ClockifyWorkspace.objects.all():
        response = requests.get(
            f"{CLOCKIFY_API_BASE}/workspaces/{workspace.workspace_id}/projects/",
            headers=headers
        )

        if response.status_code != 200:
            print(f"⚠️ Failed to fetch projects for workspace {workspace.name}")
            continue

        projects = response.json()

        for project in projects:
            obj, created = ClockifyProjects.objects.update_or_create(
                project_id=project["id"],
                defaults={
                    "name": project["name"],
                    "workspace": workspace,
                }
            )
            saved_projects.append(obj)

    return saved_projects


def sync_clockify_time_entries():
    """
    Fetch and sync all users' time entries from each Clockify workspace.
    """
    api_key = settings.CLOCKIFY_API_KEY
    if not api_key:
        return {"error": "Clockify API key is missing in settings."}

    headers = {"X-Api-Key": api_key}
    saved_entries = []

    # Loop through all workspaces in your DB
    for workspace in ClockifyWorkspace.objects.all():
        # Then loop through all users in this workspace
        users = ClockifyUsers.objects.filter(workspace=workspace)
        for user in users:
            url = f"{CLOCKIFY_API_BASE}/workspaces/{workspace.workspace_id}/user/{user.user_id}/time-entries"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"⚠️ Failed to fetch time entries for workspace {workspace.name}, user {user.name}")
                continue

            time_entries = response.json()

            for entry in time_entries:
                time_interval = entry.get("timeInterval", {})
                start_dt = parse_datetime(time_interval.get("start")) if time_interval.get("start") else None
                end_dt = parse_datetime(time_interval.get("end")) if time_interval.get("end") else None
                duration = time_interval.get("duration")

                project = ClockifyProjects.objects.filter(project_id=entry.get("projectId")).first()

                obj, created = ClockifyTimeEntry.objects.update_or_create(
                    time_entry_id=entry["id"],
                    defaults={
                        "user": user,
                        "project": project,
                        "description": entry.get("description", ""),
                        "start": start_dt,
                        "end": end_dt,
                        "duration": duration,
                    }
                )
                obj.save(update_fields=["updated_at"])
                saved_entries.append(obj)

    return saved_entries
