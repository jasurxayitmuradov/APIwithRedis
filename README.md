# Weather API (Django + DRF + Redis Cache)

This project fetches weather data by city from an external API and stores the result in Redis cache.

## About the Project

The service works as follows:

1. The client sends a request to `GET /api/weather/<city>/`.
2. The server first checks Redis cache.
3. If not found, it fetches data from the Visual Crossing API.
4. The response is cached for 12 hours (`43200` seconds).

As a result, repeated requests for the same city return faster.

## Technologies

- Python 3.12+
- Django 6
- Django REST Framework
- Redis
- django-redis
- requests
- python-dotenv

## Project Structure

```text
redis_api/
├── requirements.txt
├── .gitignore
├── README.md
└── weather/
    ├── manage.py
    ├── db.sqlite3
    ├── weather/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    └── weather_app/
        ├── views.py
        ├── urls.py
        └── ...
```

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Redis (locally on `127.0.0.1:6379`):

```bash
redis-server
```

4. Go to the `weather/` directory and run migrations:

```bash
cd weather
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

## Environment Variables (`.env`)

Create a `weather/.env` file:

```env
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_URL=redis://127.0.0.1:6379/1
```

If `REDIS_URL` is not set, the default value `redis://127.0.0.1:6379/1` is used.

## API Endpoint

### Get Weather

- Method: `GET`
- URL: `/api/weather/<city>/`
- Example:

```http
GET http://127.0.0.1:8000/api/weather/Tashkent/
```

### Sample Response (from API)

```json
{
  "source": "api",
  "data": {
    "...": "..."
  }
}
```

### Sample Response (from Cache)

```json
{
  "source": "cache",
  "data": {
    "...": "..."
  }
}
```

## Current Limitations

- Tests are not implemented yet (`weather_app/tests.py` is empty).
- `DEBUG=True` and `SECRET_KEY` are in code; production should use separate secure configuration.
- The 404 response in `views.py` may expose the API key; it should be revised for production.

## Useful Commands

```bash
# Django check
python manage.py check

# Tests
python manage.py test
```
