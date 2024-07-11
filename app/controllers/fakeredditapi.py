import requests
from dotenv import load_dotenv
import os

load_dotenv()


class FakeRedditAPI:
    BASE_URL = f'{os.getenv("FEDDIT_SERVICE_URL")}/api/v1'
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_version(self):
        url = f"{self.BASE_URL}/version"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
        
    def get_subfeddits(self, skip=0, limit=10):
        url = f"{self.BASE_URL}/subfeddits"
        params = {"skip": skip, "limit": limit}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_subfeddit_info(self, subfeddit_id):
        url = f"{self.BASE_URL}/subfeddit"
        params = {"subfeddit_id": subfeddit_id}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_comments(self, subfeddit_id, skip=0, limit=25, page=0):
        url = f"{self.BASE_URL}/comments"
        if (skip == 0) and (page > 0):
            skip = limit * (page-1)
        params = {"subfeddit_id": subfeddit_id, "skip": skip, "limit": limit}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    
    