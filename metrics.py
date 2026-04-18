import prometheus_client
from prometheus_client import Gauge

# General Global Metrics
CHALLENGES_TOTAL = Gauge('ctfd_challenges_total', 'The total number of challenges')
CHALLENGES_POINTS_TOTAL = Gauge('ctfd_challenges_points_total', 'The total amount of available points')
UNIQUE_IPS = Gauge('ctfd_unique_ips', 'Number of unique IPs that have submitted flags')

# Team Metrics
TEAMS_TOTAL = Gauge('ctfd_teams_total', 'The total number of registered teams')
TEAM_INFO = Gauge('ctfd_team_info', 'Metadata for a team (labels contain the info)', ['team_id', 'team_name', 'email', 'website', 'affiliation', 'country', 'members'])

# User Metrics
USERS_TOTAL = Gauge('ctfd_users_total', 'Total number of registered users')
USER_INFO = Gauge('ctfd_user_info', 'Metadata for a user (labels contain the info)', ['user_id', 'user_name', 'email', 'website', 'affiliation', 'country', 'team_id'])

# Challenge Metrics
CHALLENGE_SOLVES = Gauge('ctfd_challenge_solves', 'The amount of solves per challenge', ['category', 'id', 'challenge_name', 'value'])

# Submissions Metrics
SUBMISSION_FAILS = Gauge('ctfd_submission_fails', 'Number of incorrect submissions per task', ['category', 'id', 'challenge_name'])
SUBMISSION_SOLVES = Gauge('ctfd_submission_solves', 'Number of correct submissions per task', ['category', 'id', 'challenge_name'])
SUBMISSIONS_FAILS_TOTAL = Gauge('ctfd_submissions_fails_total', 'Total number of incorrect submissions')
SUBMISSIONS_SOLVES_TOTAL = Gauge('ctfd_submissions_solves_total', 'Total number of correct submissions')
SUBMISSIONS_TOTAL = Gauge('ctfd_submissions_total', 'Total number of submissions')
SUBMISSIONS_DETAILED = Gauge(
    'ctfd_submissions_detailed',
    'Total number of submissions by challenge, team, user, and type',
    ['challenge_id', 'challenge_name', 'team_id', 'team_name', 'user_id', 'user_name', 'type']
)

# Scoreboard Metrics
USER_SCORE = Gauge('ctfd_user_score', 'Score per user on the scoreboard', ['user_name', 'team_name'])
TEAM_SCORE = Gauge('ctfd_team_score', 'Score per team on the scoreboard', ['team_name'])

# Advanced CTFd Content (Hints, Awards)
HINTS_TOTAL = Gauge('ctfd_hints_total', 'Total number of hints created')
HINT_INFO = Gauge('ctfd_hint_info', 'Cost and metadata for hints', ['hint_id', 'challenge_id', 'cost'])
AWARDS_POINTS = Gauge('ctfd_award_points', 'Points awarded to users/teams manually', ['name', 'team_id', 'team_name', 'user_id', 'user_name'])
