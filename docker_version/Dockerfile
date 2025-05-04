FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      portaudio19-dev \
      python3-pyaudio \
      ffmpeg \
      pulseaudio-utils \
      libpulse0 \
      libasound2-plugins \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5050

# Tell ALSA/Pulse where to find the WSL audio socket
ENV PULSE_SERVER=unix:/mnt/wslg/PulseServer

CMD ["python", "app.py"]
