import logging
from metrics import (
    SUBMISSIONS_DETAILED, UNIQUE_IPS, SUBMISSIONS_SOLVES_TOTAL,
    SUBMISSIONS_FAILS_TOTAL, SUBMISSIONS_TOTAL,
    CHALLENGE_SOLVES, SUBMISSION_SOLVES, SUBMISSION_FAILS
)

def collect_submissions(client, chal_map, team_map, user_map, counts_map):
    try:
        submissions = client.get_paginated_data("/api/v1/submissions")
        
        new_counts_map = {}
        chal_solves_count = {}
        chal_fails_count = {}
        unique_ips = set()
        global_solves = 0
        global_fails = 0
        
        for sub in submissions:
            c_id = str(sub.get('challenge_id', ''))
            t_id = str(sub.get('team_id', ''))
            u_id = str(sub.get('user_id', ''))
            s_type = sub.get('type', 'unknown')
            ip = sub.get('ip', '')
            
            if ip:
                unique_ips.add(ip)

            key = (c_id, t_id, u_id, s_type)
            new_counts_map[key] = new_counts_map.get(key, 0) + 1

            if s_type == 'correct':
                chal_solves_count[c_id] = chal_solves_count.get(c_id, 0) + 1
                global_solves += 1
            elif s_type == 'incorrect':
                chal_fails_count[c_id] = chal_fails_count.get(c_id, 0) + 1
                global_fails += 1
                
        # Update metrics
        UNIQUE_IPS.set(len(unique_ips))
        SUBMISSIONS_SOLVES_TOTAL.set(global_solves)
        SUBMISSIONS_FAILS_TOTAL.set(global_fails)
        SUBMISSIONS_TOTAL.set(len(submissions))
        
        # Expert Detailed Metrics
        for key, count in new_counts_map.items():
            c_id, t_id, u_id, s_type = key
            c_data = chal_map.get(c_id, {})
            c_name = c_data.get('name', f"Chal_{c_id}")
            t_name = team_map.get(t_id, f"Team_{t_id}") if t_id and t_id != 'None' else "No_Team"
            u_name = user_map.get(u_id, f"User_{u_id}") if u_id and u_id != 'None' else "No_User"
            
            SUBMISSIONS_DETAILED.labels(
                challenge_id=c_id, challenge_name=c_name, team_id=t_id, team_name=t_name,
                user_id=u_id, user_name=u_name, type=s_type
            ).set(count)
            
        # Clear out old mappings to avoid memleaks
        for old_key in counts_map:
            if old_key not in new_counts_map:
                c_id, t_id, u_id, s_type = old_key
                c_data = chal_map.get(c_id, {})
                c_name = c_data.get('name', f"Chal_{c_id}")
                t_name = team_map.get(t_id, f"Team_{t_id}") if t_id and t_id != 'None' else "No_Team"
                u_name = user_map.get(u_id, f"User_{u_id}") if u_id and u_id != 'None' else "No_User"
                try:
                    SUBMISSIONS_DETAILED.labels(
                        challenge_id=c_id, challenge_name=c_name, team_id=t_id, team_name=t_name,
                        user_id=u_id, user_name=u_name, type=s_type
                    ).set(0)
                except Exception:
                    pass
                    
        # Update Challenge-Specific Simple Metrics
        for c_id, c_data in chal_map.items():
            c_name = c_data.get('name', f"Chal_{c_id}")
            c_cat = c_data.get('category', 'unknown')
            c_val = str(c_data.get('value', 0))
            
            solves = chal_solves_count.get(c_id, 0)
            fails = chal_fails_count.get(c_id, 0)
            
            CHALLENGE_SOLVES.labels(category=c_cat, id=c_id, challenge_name=c_name, value=c_val).set(solves)
            SUBMISSION_SOLVES.labels(category=c_cat, id=c_id, challenge_name=c_name).set(solves)
            SUBMISSION_FAILS.labels(category=c_cat, id=c_id, challenge_name=c_name).set(fails)
            
        return submissions, new_counts_map
    except Exception as e:
        logging.error(f"Failed to collect submissions: {e}")
        return [], counts_map
