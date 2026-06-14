# promptkeep

A self-hostable LLM request logger. FastAPI service that proxies prompts to [Groq](https://groq.com) and persists every prompt/response pair to PostgreSQL with latency metrics — useful for building evaluation datasets, debugging prompt regressions, or analyzing model behavior over time.

Fully containerized with Docker Compose. Published image available on [GitHub Container Registry](https://github.com/abdulsgilal579/promptkeep/pkgs/container/promptkeep-api).

## Features

- `POST /generate` — send a prompt, get a Groq completion back
- `GET /logs` — retrieve recent requests with latency metrics
- Automatic logging of every call to Postgres (model, prompt, output, latency, timestamp)
- Interactive API docs at `/docs` (Swagger UI)
- Healthchecked Postgres, named volumes for persistence

## Tech stack

| Layer | Choice |
|---|---|
| API | FastAPI + Pydantic (Python 3.12) |
| Inference | Groq API (LLaMA 3.1, configurable per request) |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy |
| Containers | Docker + Compose |
| Registry | GitHub Container Registry (GHCR) |

## Quick start (no source code needed)

Requirements: Docker installed, and a Groq API key from [console.groq.com](https://console.groq.com).

```bash
mkdir promptkeep && cd promptkeep
curl -O https://raw.githubusercontent.com/abdulsgilal579/promptkeep/main/docker-compose.yml
echo "GROQ_API_KEY=your_groq_key_here" > .env
docker compose up
```

Visit http://localhost:8000/docs to interact with the API.

## Usage

Send a prompt:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain attention in transformers in one paragraph."}'
```

Response:

```json
{
  "output": "Attention is the mechanism by which...",
  "model": "llama-3.1-8b-instant",
  "latency_ms": 387.4
}
```

View all logged requests:

```bash
curl http://localhost:8000/logs
```

Use a different model:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "...", "model": "llama-3.3-70b-versatile"}'
```

See [Groq's model catalog](https://console.groq.com/docs/models) for the current list.

## Develop from source

```bash
git clone https://github.com/abdulsgilal579/promptkeep.git
cd promptkeep
cp .env.example .env  # then edit and add your GROQ_API_KEY
docker compose up --build
```

Edit code in `app/`, then run `docker compose up --build` to rebuild. Docker's layer caching means code-only changes rebuild in ~2 seconds.

## Architecture

```
┌─────────┐         ┌──────────────┐         ┌──────────┐
│ Client  │ ──────► │  FastAPI     │ ──────► │ Groq API │
│ (curl,  │         │  :8000       │         │ (cloud)  │
│  curl,  │ ◄────── │              │         └──────────┘
│  curl)  │         │              │
└─────────┘         │              │
                    │              │ ──────► ┌──────────┐
                    └──────────────┘         │ Postgres │
                                             │  :5432   │
                                             └──────────┘
                  ┌─────── Compose network ─────────┐
```

Two containers on a private Compose network. The API is the only service exposed to the host (port 8000). Postgres is internal-only, reachable only by the API. Data persists across container restarts via a named volume.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | _(required)_ | API key from console.groq.com |
| `DATABASE_URL` | `postgresql://promptkeep:promptkeep@postgres:5432/promptkeep` | Postgres connection string |

## Useful commands

```bash
docker compose up -d           # start in background
docker compose logs -f         # tail logs from all services
docker compose ps              # see what's running
docker compose down            # stop and remove containers (volumes survive)
docker compose down -v         # also wipe Postgres data
```

## License

MIT
