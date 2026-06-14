# promptkeep

A FastAPI service that logs every LLM call to Postgres, with Groq as the inference backend. Fully containerized.

## Run with Docker (no source code needed)

```bash
curl -O https://raw.githubusercontent.com/abdulsgilal579/promptkeep/main/docker-compose.yml
echo "GROQ_API_KEY=your_groq_key" > .env
docker compose up
```

Then visit http://localhost:8000/docs

## Run from source

```bash
git clone https://github.com/abdulsgilal579/promptkeep.git
cd promptkeep
cp .env.example .env  # add your GROQ_API_KEY
docker compose up --build
```
