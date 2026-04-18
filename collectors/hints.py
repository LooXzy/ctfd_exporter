import logging
from metrics import HINTS_TOTAL, HINT_INFO

def collect_hints(client):
    try:
        HINT_INFO.clear()
        
        # 1. Collect Hints (costs and definitions)
        hints_data = client.get_paginated_data("/api/v1/hints")
        HINTS_TOTAL.set(len(hints_data))
        
        for h in hints_data:
            h_id = str(h.get('id', ''))
            c_id = str(h.get('challenge_id', ''))
            cost = str(h.get('cost', 0) or 0)
            
            HINT_INFO.labels(hint_id=h_id, challenge_id=c_id, cost=cost).set(1)
            
    except Exception as e:
        logging.error(f"Failed to collect hints: {e}")
