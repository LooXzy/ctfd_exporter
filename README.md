# CTFd Exporter (Prometheus)

Un exporteur Prometheus écrit en Python pour récupérer les statistiques depuis l'API de CTFd.

## Installation
1. Créez un fichier `.env` en vous basant sur le `.env.example` :
   ```bash
   cp .env.example .env
   ```

2. Éditez le fichier `.env` :
   - `CTFD_URL` : L'URL racine de votre instance CTFd.
   - `CTFD_TOKEN` : Un token d'accès administrateur de CTFd.
   - `POLL_INTERVAL` : Temps d'attente (en secondes) entre deux requêtes successives de scrapping vers l'API. (Par défaut : 30).

3. Déployez l'application via Docker Compose avec la commande suivante :
    ```bash
    docker-compose up -d --build
    ```
    L'exporteur sera accessible à l'adresse suivante : `http://localhost:8000/metrics`.

## Intégration Prometheus
Ajoutez la cible dans votre configuration `prometheus.yml` :

```yaml
scrape_configs:
  - job_name: 'ctfd_exporter'
    scrape_interval: 10s
    static_configs:
      - targets: ['votre-serveur:8000']
```

## Métriques disponibles
**Informations générales :**
- `ctfd_challenges_total` : Nombre total de challenges
- `ctfd_challenges_points_total` : Total des points disponibles 
- `ctfd_teams_total` : Nombre de d'équipes enregistrées
- `ctfd_team_info` : Métrique contenant les informations de l'équipe dans ses labels (`team_id`, `team_name`, `email`, `website`, `affiliation`, `country`, `members`)
- `ctfd_users_total` : Nombre d'utilisateurs enregistrés
- `ctfd_user_info` : Métrique contenant les informations de l'utilisateur dans ses labels (`user_id`, `user_name`, `email`, `website`, `affiliation`, `country`, `team_id`)
- `ctfd_unique_ips` : Nombre d'IPs uniques ayant interagi

**Scoreboard :**
- `ctfd_user_score` : Score par utilisateur (avec labels: `user_name`, `team_name`)
- `ctfd_team_score` : Score par équipe (avec labels: `team_name`)

**Soumissions :**
- `ctfd_challenge_solves` : Nombre de validations par challenge (labels: `category`, `id`, `challenge_name`, `value`)
- `ctfd_submission_fails` : Échecs (`incorrect`) par tâche (labels: `category`, `id`, `challenge_name`)
- `ctfd_submission_solves` : Validations (`correct`) par tâche (labels: `category`, `id`, `challenge_name`)
- `ctfd_submissions_fails_total` : Total global incorrect
- `ctfd_submissions_solves_total` : Total global correct
- `ctfd_submissions_total` : Total des soumissions globales
- `ctfd_submissions_detailed` : Combine tout ! Comptabilise les essais avec les labels croisés suivants pour chaque métrique :
  - `challenge_id` et `challenge_name`
  - `team_id` et `team_name`
  - `user_id` et `user_name`
  - `type` (`correct` ou `incorrect`)

**Contenu Avancé CTFd (Points manuels et Indices) :**
- `ctfd_hints_total` : Le nombre total d'indices créés sur la plateforme
- `ctfd_hint_info` : Métrique contenant les IDs, challenge associés et le coût en points d'un indice (avec labels: `hint_id`, `challenge_id`, `cost`)
- `ctfd_award_points` : Les points additionnels donnés manuellement (Awards), par exemple pour les Writeups (avec labels: `name`, `team_id`, `team_name`, `user_id`, `user_name`)