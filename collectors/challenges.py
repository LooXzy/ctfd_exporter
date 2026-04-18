import logging
from metrics import CHALLENGES_TOTAL, CHALLENGES_POINTS_TOTAL

def collect_challenges(client):
    try:
        challenges_data = client.get_paginated_data("/api/v1/challenges")
        chal_map = {str(c['id']): c for c in challenges_data}
        
        # Update metrics
        CHALLENGES_TOTAL.set(len(challenges_data))
        
        total_points = sum(int(c.get('value', 0) or 0) for c in challenges_data)
        CHALLENGES_POINTS_TOTAL.set(total_points)
        
        return chal_map
    except Exception as e:
        logging.error(f"Failed to collect challenges: {e}")
        return {}
