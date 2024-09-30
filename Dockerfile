# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid Python buffering (optional, for faster logging)
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app will run on (Flask by default runs on port 5000, change if needed)
EXPOSE 3003

# Set the entrypoint to run the Flask app (ensure scrapper.py is the correct file)
CMD if [ "$FLASK_ENV" = "development" ]; then \
    pip install watchdog && flask --app scrapper run --host=0.0.0.0 --port=3003 --reload; \
else \
    python scrapper.py; \
fi
