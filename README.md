# Weather Stations API

A FastAPI application for processing and serving weather station temperature statistics.

## Tech Stack

- **FastAPI** - Web framework
- **Redis** - Caching layer
- **JWT** - Authentication
- **Docker** - Containerization

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Environment Variables

For easier setup, the following `.env` file has been committed to the repository:
```env
REDIS_URL=redis://redis:6379/0
VALID_USERNAME=admin
VALID_PASSWORD=password
SECRET_KEY=secret-key-123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CSV_HOST_PATH=/path/to/your/measurements.csv
CSV_FILE_PATH=/app/measurements.csv
```

**Note:** The `measurements.csv` file is not included due to its size. Update `CSV_HOST_PATH` to point to your CSV file on your machine.

### Running the Application

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8010`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Authenticate and get JWT token |
| POST | `/api/auth/logout` | Invalidate token |

### Weather Data

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/weather/cities` | List temperature stats for all cities |
| GET | `/api/weather/city?name={city}` | Get temperature stats for a specific city |
| GET | `/api/weather/averages/{temp}?operator={op}` | Filter cities by average temperature |
| POST | `/api/weather/reload` | Reload stats from CSV |
| POST | `/api/weather/clear_cache` | Clear Redis cache |

**Note:** All weather endpoints require authentication via Bearer token.

## Authentication

1. Login to get a token:
- The credentials are:
```json
{
  "username": "admin",
  "password": "password"
}
```
```bash
curl -X POST "http://localhost:8010/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

2. Use the token in requests:
```bash
curl "http://localhost:8010/api/weather/cities" \
  -H "Authorization: Bearer <your_token>"
```

## API Documentation

Interactive docs available at:
- Swagger UI: `http://localhost:8010/docs`