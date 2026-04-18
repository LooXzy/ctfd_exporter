import logging
from metrics import USER_SCORE, TEAM_SCORE

def collect_scoreboard(client):
    try:
        USER_SCORE.clear()
        TEAM_SCORE.clear()
        
        scoreboard_data = client.get_paginated_data("/api/v1/scoreboard")
        
        for entry in scoreboard_data:
            score = entry.get('score', 0)
            name = entry.get('name', 'unknown')
            
            # Identify if it's a team mode scoreboard or user mode scoreboard
            # Teams usually have 'members' or 'account_id' in their scoreboard entries in CTFd Team mode
            if 'members' in entry or 'team_id' in entry:
                TEAM_SCORE.labels(team_name=name).set(score)
                # Parse the inner members
                for member in entry.get('members', []):
                    m_score = member.get('score', 0)
                    m_name = member.get('name', 'unknown')
                    USER_SCORE.labels(user_name=m_name, team_name=name).set(m_score)
            else:
                USER_SCORE.labels(user_name=name, team_name="None").set(score)
    except Exception as e:
        logging.error(f"Failed to collect scoreboard: {e}")
