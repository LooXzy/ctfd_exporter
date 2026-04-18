import requests
import logging

class CTFdClient:
    def __init__(self, url, token):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get_paginated_data(self, endpoint, params=None):
        if params is None:
            params = {}
        
        results = []
        page = 1
        while True:
            params['page'] = page
            if 'per_page' not in params:
                params['per_page'] = 100
            
            full_url = f"{self.url}{endpoint}"
            try:
                resp = self.session.get(full_url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                
                if not data.get("success"):
                    logging.warning(f"Failed to fetch {endpoint}: {data}")
                    break
                    
                items = data.get("data", [])
                if not items:
                    break
                    
                results.extend(items)
                
                meta = data.get("meta", {})
                pagination = meta.get("pagination", {})
                if pagination.get("next_page") is None and len(items) < params['per_page']:
                    break
                    
            except Exception as e:
                logging.error(f"Error fetching {endpoint} page {page}: {e}")
                break
                
            page += 1
            
        return results
