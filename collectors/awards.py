import logging
from metrics import AWARDS_POINTS

def collect_awards(client, team_map, user_map, counts_map):
    try:
        data = client.get_paginated_data("/api/v1/awards")
        new_counts_map = {}
        for award in data:
            a_name = str(award.get('name', 'Unknown'))
            t_id = str(award.get('team_id', ''))
            u_id = str(award.get('user_id', ''))
            val_raw = award.get('value')
            val = int(val_raw) if val_raw is not None else 0
            
            key = (a_name, t_id, u_id)
            new_counts_map[key] = new_counts_map.get(key, 0) + val
            
        for key, points in new_counts_map.items():
            a_name, t_id, u_id = key
            t_name = team_map.get(t_id, f"Team_{t_id}") if t_id and t_id != 'None' else "No_Team"
            u_name = user_map.get(u_id, f"User_{u_id}") if u_id and u_id != 'None' else "No_User"
            AWARDS_POINTS.labels(
                name=a_name, team_id=t_id, team_name=t_name,
                user_id=u_id, user_name=u_name
            ).set(points)
            
        # Cleanup old references
        for old_key in counts_map:
            if old_key not in new_counts_map:
                a_name, t_id, u_id = old_key
                t_name = team_map.get(t_id, f"Team_{t_id}") if t_id and t_id != 'None' else "No_Team"
                u_name = user_map.get(u_id, f"User_{u_id}") if u_id and u_id != 'None' else "No_User"
                try:
                    AWARDS_POINTS.labels(
                        name=a_name, team_id=t_id, team_name=t_name,
                        user_id=u_id, user_name=u_name
                    ).set(0)
                except Exception:
                    pass
                    
        return new_counts_map
    except Exception as e:
        logging.error(f"Failed to collect awards: {e}")
        return counts_map
