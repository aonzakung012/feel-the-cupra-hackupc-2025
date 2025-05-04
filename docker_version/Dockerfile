# 1. Start from official slim Python image
FROM python:3.9-slim

# 2. Install system deps: PortAudio, PyAudio bindings, FFmpeg, build tools
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      portaudio19-dev \
      python3-pyaudio \
      ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# 3. Set working dir
WORKDIR /app

# 4. Copy & install Python libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Expose Flask’s port
EXPOSE 5000

# 7. Start the app
CMD ["python", "app.py"]
