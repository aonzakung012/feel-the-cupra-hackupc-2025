#flask
import os
import wave
import glob
import tempfile
import asyncio
from collections import deque

from flask import Flask
import pyaudio
from dotenv import load_dotenv

from class_bot import GeminiLiveAssistant

load_dotenv()

# init assistant
assistant = GeminiLiveAssistant(
    system_instruction=(
        "You are a helpful english assistant who only answers based on the CUPRA Tavascan 2024 owner's manual. "
        "Be concise. Do not offer extra help unless asked. "
        "If you don't understand the question ask politely if the user can repeat it."
    )
)

# ensure output folder exists
BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE, "audio_outputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# audio params
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 4

p = pyaudio.PyAudio()

def record_audio_to_wav(duration=RECORD_SECONDS) -> str:
    """Record `duration` seconds and write to a temp WAV, returning its path."""
    print("🎙️  Recording...")
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * duration))]
    stream.stop_stream()
    stream.close()
    print("✅ Recording done.")
    
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wf = wave.open(tf.name, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    return tf.name

async def one_iteration():
    # 1) user → text
    in_wav = record_audio_to_wav()
    user_text = await assistant.transcribe_audio(in_wav)
    print("User (transcript)>", user_text)

    # 2) text → assistant audio + playback
    resp_path = os.path.join(OUTPUT_FOLDER, f"response_{hash(user_text)%10000}.wav")
    out_wav = await assistant.chat_and_play(user_text, output_wav=resp_path)

    # 3) assistant audio → text
    reply_text = await assistant.transcribe_audio(out_wav)
    print("Assistant (transcript)>", reply_text)

app = Flask(__name__)

@app.route("/listen", methods=["GET"])
def listen():
    # run the entire flow in its own event loop
    asyncio.run(one_iteration())
    # return no content
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5050)))
