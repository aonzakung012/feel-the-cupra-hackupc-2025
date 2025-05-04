from class_bot import GeminiLiveAssistant
import asyncio
import os
import glob
import tempfile
import pyaudio
import wave
from dotenv import load_dotenv

load_dotenv()

# --- Audio setup ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 4

p = pyaudio.PyAudio()


def record_audio_to_wav(duration=RECORD_SECONDS):
    print("🎙️ Speak now...")
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * duration))]
    stream.stop_stream()
    stream.close()
    print("✅ Recording done.")
    
    # Save to temp WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        wf = wave.open(temp_audio.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return temp_audio.name

def delete_wav(output_folder):
    # Clean up all .wav files in the output folder
    for wav_file in glob.glob(os.path.join(output_folder, "*.wav")):
        try:
            os.remove(wav_file)
        except Exception as e:
            print(f"Failed to delete {wav_file}: {e}")
    print(f"\n 🗑️  All the .wav files are deleted")


if __name__ == "__main__":

    assistant = GeminiLiveAssistant(
        system_instruction=(
            "You are a helpful english assistant who only answers based on the CUPRA Tavascan 2024 owner's manual. "
            "Be concise. Do not offer extra help unless asked."
            "If you don't understand the question ask politely if the user can repeat it."
            "Answer the user question."
        )
    )

    async def run_examples():

        base_folder = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(base_folder, "audio_outputs")
        os.makedirs(output_folder, exist_ok=True)

        first_time = True

        while True:
            if first_time:
                print("\nWelcome to the AI Assistant of the CUPRA Tavascan 2024! Type 'exit' to quit anytime.")
                print("\nPress Enter to ask a question by voice or type your question.\n")
                first_time = False

            cmd = input("\nUser> ").strip()
            
            if cmd.lower() == "exit":
                delete_wav(output_folder)
                break
            
            # Record voice
            if cmd == "":  
                file_path = record_audio_to_wav()
                message = await assistant.transcribe_audio(file_path)
                print("User (voice)> ", message)
            elif cmd.lower() == "l":
                file_path = record_audio_to_wav(duration=8)
                message = await assistant.transcribe_audio(file_path)
                print("User (voice)> ", message)
            else:
                message = cmd  # text input
            
            if message.lower() == "exit":
                delete_wav(output_folder)
                break
            
            # Unique response path
            response_path = os.path.join(output_folder, f"response_{hash(message) % 10000}.wav")

            # text → audio playback
            wav_file = await assistant.chat_and_play(message, output_wav=response_path) 
    

            # audio → text transcript
            transcript = await assistant.transcribe_audio(wav_file)
            print("Assistant>", transcript)

    asyncio.run(run_examples())