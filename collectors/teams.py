import logging
from metrics import TEAMS_TOTAL, TEAM_INFO

def collect_teams(client):
    try:
        TEAM_INFO.clear()
        teams_data = client.get_paginated_data("/api/v1/teams")
        team_map = {str(t['id']): t.get('name', f"Team_{t['id']}") for t in teams_data}
        
        # Update metrics
        TEAMS_TOTAL.set(len(teams_data))
        
        for t in teams_data:
            t_id = str(t.get('id', ''))
            t_name = str(t.get('name', f"Team_{t_id}"))
            email = str(t.get('email') or '')
            website = str(t.get('website') or '')
            affiliation = str(t.get('affiliation') or '')
            country = str(t.get('country') or '')
            
            # Members might be a list of user IDs or objects depending on admin privileges
            members_raw = t.get('members', [])
            members = ",".join([str(m) for m in members_raw])
            
            TEAM_INFO.labels(
                team_id=t_id, team_name=t_name, email=email, website=website,
                affiliation=affiliation, country=country, members=members
            ).set(1)
            
        return team_map
    except Exception as e:
        logging.error(f"Failed to collect teams: {e}")
        return {}
