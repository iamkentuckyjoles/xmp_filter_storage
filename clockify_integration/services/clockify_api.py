import requests
from django.conf import settings
from datetime import datetime, timedelta
import json

class ClockifyAPI:
    BASE_URL = "https://api.clockify.me/api/v1"
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_workspaces(self):
        url = f"{self.BASE_URL}/workspaces"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_users(self, workspace_id):
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/users"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_projects(self, workspace_id):
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/projects"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_time_entries(self, workspace_id, user_id, start_date, end_date):
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/user/{user_id}/time-entries"
        params = {
            "start": start_date.isoformat() + "Z",
            "end": end_date.isoformat() + "Z"
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def get_detailed_report(self, workspace_id, date_range_start, date_range_end):
        url = f"{self.BASE_URL}/workspaces/{workspace_id}/reports/detailed"
        
        payload = {
            "dateRangeStart": date_range_start.isoformat() + "Z",
            "dateRangeEnd": date_range_end.isoformat() + "Z",
            "detailedFilter": {
                "page": 1,
                "pageSize": 1000
            },
            "exportType": "JSON"
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()