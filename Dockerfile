FROM python:3.12-slim

WORKDIR /app

# Copy requirements FIRST and install — this layer is cached
# until requirements.txt changes, so code edits don't trigger reinstall
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the app code (changes often, so it's a later layer)
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]