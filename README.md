# CyberGuard — Advanced Cybersecurity Training Platform

CyberGuard is an interactive cybersecurity awareness and simulation platform.

## Included
- Next.js frontend for Vercel
- Django REST backend for Render
- PostgreSQL-ready configuration
- JWT authentication and user/admin roles
- Resumable server-side training sessions
- Adaptive difficulty metadata and security risk profile
- Phishing, URL, password and malware simulations
- Incident Response simulation lab
- XP, levels, badges and leaderboard
- Advanced admin analytics
- Gemini-powered CyberGuard AI Coach
- Defensive-only AI safety instructions

## Local backend
```bash
cd backend
python -m venv .venv
# activate the environment
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Set `GEMINI_API_KEY` only on the backend. Never expose it as a `NEXT_PUBLIC_*` variable.

## Render
Root directory: `backend`
Build:
`pip install -r requirements.txt && python manage.py collectstatic --noinput`
Start:
`gunicorn config.wsgi:application`

Environment variables:
`DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `FRONTEND_URL`, `DATABASE_URL`, `GEMINI_API_KEY`, `GEMINI_MODEL`.

After deployment:
`python manage.py migrate`
`python manage.py seed_demo`

## Vercel
Root directory: `frontend`
Framework: Next.js
Environment:
`NEXT_PUBLIC_API_URL=https://YOUR-RENDER-HOST/api`

Do not set a `public` output directory.
