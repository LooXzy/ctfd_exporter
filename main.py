import time
import logging
from prometheus_client import start_http_server
from config import CTFD_URL, CTFD_TOKEN, PORT, POLL_INTERVAL
from client import CTFdClient
from collectors.challenges import collect_challenges
from collectors.teams import collect_teams
from collectors.users import collect_users
from collectors.scoreboard import collect_scoreboard
from collectors.submissions import collect_submissions
from collectors.hints import collect_hints
from collectors.awards import collect_awards

def main():
    start_http_server(PORT)
    logging.info(f"CTFd Prometheus Exporter started on port {PORT}.")
    logging.info(f"Target CTFd: {CTFD_URL}")
    logging.info(f"Polling interval: {POLL_INTERVAL}s")
    
    client = CTFdClient(CTFD_URL, CTFD_TOKEN)
    sub_counts = {}
    award_counts = {}
    
    while True:
        try:
            logging.info("Starting polling cycle...")
            
            # Fetch dimensions
            chal_map = collect_challenges(client)
            team_map = collect_teams(client)
            user_map = collect_users(client)
            
            # Fetch metrics
            collect_scoreboard(client)
            collect_hints(client)
            
            # Fetch & compute complex mapped metrics
            submissions, sub_counts = collect_submissions(
                client=client, chal_map=chal_map, team_map=team_map, user_map=user_map, counts_map=sub_counts
            )
            
            award_counts = collect_awards(
                client=client, team_map=team_map, user_map=user_map, counts_map=award_counts
            )
            
            logging.info(f"Polling cycle complete. Processed {len(submissions)} raw submissions.")
        except Exception as e:
            logging.error(f"Critical error during polling cycle loop: {e}", exc_info=True)
            
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
