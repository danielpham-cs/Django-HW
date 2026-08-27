# 🧭 Tourist Attraction Recommendation Website

A Django web app for a tourist-attraction recommendation site. It manages three
tables — **User**, **Tourist Attraction (Spot)**, and **Rating** — with full
**insert / update / delete** support using both **GET** and **POST** requests,
a clean front-end, and a Docker setup.

## Database Schema

| Table | Fields |
|-------|--------|
| **User** (`Visitor`) | `id`, `name`, `age` |
| **Tourist Attraction** (`Spot`) | `id`, `name`, `location`, `category` (Area / Category) |
| **Rating** | `id`, `visitor` → User, `spot` → Attraction, `score` (1–5), `comment` |

`Rating` links a `User` to a `Spot` via foreign keys.

## Features

- List, create, edit, and delete records for all three tables.
- **GET** requests render list pages and pre-filled forms; **POST** requests
  perform the create / update / delete write actions (CSRF-protected).
- Responsive front-end (custom CSS, no external dependencies).
- Sample data auto-loaded on first run.
- Django admin available at `/admin/`.

## How to Run

### Option A — Docker (recommended)

Requires Docker + Docker Compose.

```bash
# from the project root (this folder)
docker compose up --build
```

Then open <http://localhost:8000>.

The container automatically runs migrations, loads sample data, and starts the
server on port 8000.

To stop:

```bash
docker compose down
```

### Option B — Run locally (without Docker)

Requires Python 3.11+.

```bash
# 1. (optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. set up the database and sample data
python manage.py migrate
python manage.py seed_data

# 4. start the server
python manage.py runserver
```

Then open <http://localhost:8000>.

### Create an admin user (optional)

```bash
python manage.py createsuperuser
```

Then log in at <http://localhost:8000/admin/>.

## URL Map

| Path | Method(s) | Action |
|------|-----------|--------|
| `/` | GET | Home dashboard |
| `/users/` | GET | List users |
| `/users/add/` | GET, POST | Create user |
| `/users/<id>/edit/` | GET, POST | Update user |
| `/users/<id>/delete/` | GET, POST | Delete user (GET confirms, POST deletes) |
| `/spots/` … | GET, POST | Same pattern for attractions |
| `/ratings/` … | GET, POST | Same pattern for ratings |

## Project Structure

```
Django/
├── config/            # Django project (settings, urls, wsgi)
├── core/              # Main app
│   ├── models.py      # Visitor, Spot, Rating
│   ├── forms.py       # ModelForms with validation
│   ├── views.py       # CRUD views (GET + POST)
│   ├── urls.py
│   ├── admin.py
│   ├── management/commands/seed_data.py
│   ├── templates/core/
│   └── static/core/style.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
