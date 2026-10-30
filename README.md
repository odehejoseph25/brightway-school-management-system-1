# Brightway International Schools Management System
Django + PostgreSQL-ready application starter for Brightway International Schools, New Nyanya.

## Included
- Username/password sign-in using Django authentication
- Administrator / Teacher roles via `StaffProfile`
- Server-side admin-only restrictions for staff directory, fees, reports, and full data export
- Student records, staff profiles, classes, attendance, fee payments, examination results and basic reports
- Responsive web UI for desktop and mobile
- PostgreSQL configuration and Docker Compose
- PWA manifest and service worker app-shell fallback

## Run locally
Requires Python 3.11+.
1. Extract ZIP and open a terminal in this folder.
2. `python -m venv .venv` then activate it.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, set a strong `DJANGO_SECRET_KEY` (load env variables into your shell; Django does not automatically parse .env files).
5. `python manage.py makemigrations school`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8. `python manage.py runserver`
9. Open http://127.0.0.1:8000/

Create teacher/admin accounts through `/admin/`, then add a `StaffProfile` for each user and assign role `ADMIN` or `TEACHER`. A superuser has admin access automatically.

## PostgreSQL with Docker
Set `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` in the environment, then run `docker compose up --build`. For the first run, create migrations and an administrator inside the web container:
`docker compose exec web python manage.py makemigrations school`
`docker compose exec web python manage.py migrate`
`docker compose exec web python manage.py createsuperuser`

## Important production notes
This is source code, not a live hosted website. Configure a secure host, HTTPS, real domain, backups, email/password reset, monitoring and data-retention controls before using real pupil records. The PWA currently caches a small app shell but does **not** implement full offline data-entry queues or conflict-safe sync. Do not rely on it for offline writes or shared-device synchronization yet. Production requires testing of role access, database backups and child-data privacy procedures. Confirm school grading policy and academic session before use.
