## Local Development

### Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended)
- PostgreSQL
- Redis

### Setup

1. Clone the repository:
```bash
   git clone https://github.com/warrior88888/team-finder-ad.git
   cd team-finder-ad
```

2. Install dependencies:

   **With uv (recommended):**
```bash
   uv sync
```

   **With pip:**

   Create and activate a virtual environment:

   macOS / Linux:
```bash
   python3 -m venv .venv
   source .venv/bin/activate
```

   Windows:
```bash
   python -m venv .venv
   .venv\Scripts\activate
```

   Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create `.env` file from example:
```bash
   cp .env.example .env
```
   Fill in `TF__DJANGO__SECRET_KEY` and `TF__POSTGRES__PASSWORD` at minimum.

4. Apply migrations:
```bash
   uv run python manage.py migrate
   # or
   python manage.py migrate
```

5. Run the development server:
```bash
   uv run python manage.py runserver
   # or
   python manage.py runserver
```

### Code Quality
```bash
# with uv
uv run ruff check . --fix
uv run pyright
uv run pytest

# with pip
ruff check . --fix
pyright
pytest
```

### Notes

- `uv.lock` is committed to the repository — use `uv sync` to get exact dependency versions
- `requirements.txt` includes all dependencies including dev
- For production setup see `docker-compose.prod.yml`