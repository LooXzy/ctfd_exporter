import logging
from metrics import USERS_TOTAL, USER_INFO

def collect_users(client):
    try:
        USER_INFO.clear()
        users_data = client.get_paginated_data("/api/v1/users")
        user_map = {str(u['id']): u.get('name', f"User_{u['id']}") for u in users_data}
        
        # Update metrics
        USERS_TOTAL.set(len(users_data))
        
        for u in users_data:
            u_id = str(u.get('id', ''))
            u_name = str(u.get('name', f"User_{u_id}"))
            email = str(u.get('email') or '')
            website = str(u.get('website') or '')
            affiliation = str(u.get('affiliation') or '')
            country = str(u.get('country') or '')
            team_id = str(u.get('team_id') or 'None')
            
            USER_INFO.labels(
                user_id=u_id, user_name=u_name, email=email, website=website,
                affiliation=affiliation, country=country, team_id=team_id
            ).set(1)
            
        return user_map
    except Exception as e:
        logging.error(f"Failed to collect users: {e}")
        return {}
