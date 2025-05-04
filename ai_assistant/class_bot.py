import asyncio
import wave
import os
import sounddevice as sd
from collections import deque
from google.genai import types
from google import genai
from pydub import AudioSegment

##  sudo apt update
##  sudo apt install portaudio19-dev python3-pyaudio ffmpeg

class GeminiLiveAssistant:
    def __init__(
        self,
        api_key: str = None,
        model: str = "gemini-2.0-flash-live-001",
        system_instruction: str = "",
        sample_rate: int = 24000,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.sample_rate = sample_rate
        self.system_instruction = system_instruction
        self.client = genai.Client(api_key=self.api_key)

        base_folder = os.path.dirname(os.path.abspath(__file__))
        self.output_folder = os.path.join(base_folder, "audio_outputs")
        os.makedirs(self.output_folder, exist_ok=True)

    async def _playback_loop(self, stream, buffer: deque, playback_started: asyncio.Event, streaming_done_flag: dict):
        await playback_started.wait()
        while not (streaming_done_flag["done"] and not buffer):
            if buffer:
                stream.write(buffer.popleft())
            else:
                await asyncio.sleep(0.01)

    async def chat_and_play(self, prompt: str, output_wav: str = None, start_delay: float = 2.0):
        """
        Send a text prompt to the model and stream back audio.
        Plays audio through speakers and writes to `output_wav`.
        """

        if not output_wav:
            output_wav = os.path.join(self.output_folder, f"response_{hash(prompt) % 10000}.wav")


        # Prepare WAV file
        wf = wave.open(output_wav, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)

        # Prepare playback
        stream = sd.RawOutputStream(samplerate=self.sample_rate, channels=1, dtype='int16')
        stream.start()

        buffer = deque()
        playback_started = asyncio.Event()
        streaming_done_flag = {"done": False}
        play_task = asyncio.create_task(self._playback_loop(stream, buffer, playback_started, streaming_done_flag))

        config = {
            "response_modalities": ["AUDIO"],
            "system_instruction": self.system_instruction,
        }

        async with self.client.aio.live.connect(model=self.model, config=config) as session:
            first_chunk = True

            # send prompt
            await session.send_client_content(
                turns={"role":"user", "parts":[{"text": prompt}]},
                turn_complete=True
            )

            # receive audio chunks
            async for response in session.receive():
                if response.data:
                    wf.writeframes(response.data)
                    buffer.append(response.data)

                    if first_chunk:
                        first_chunk = False
                        # kick off playback after a short delay
                        asyncio.create_task(self._start_after_delay(playback_started, start_delay))

        # signal end, wait for playback finish
        streaming_done_flag["done"] = True
        await play_task

        stream.stop()
        stream.close()
        wf.close()

        return output_wav

    async def transcribe_audio(self, input_wav: str) -> str:
        """
        Send a WAV file to Gemini Live via realtime input and stream back a text transcription.
        Returns the full transcript.
        """

        # generate filename in current folder
        #
        #filename = f"temp_resampled_{hash(input_wav) % 10000}.wav"
        #resampled_wav = os.path.join(self.output_folder, filename)
#
        #self.resample_to_16k(input_wav, resampled_wav)


        # open the WAV and check format
        wf = wave.open(input_wav, "rb")
        assert wf.getnchannels() == 1 and wf.getsampwidth() == 2, "Audio must be mono 16-bit PCM"
        sr = wf.getframerate()
        # note: Live API officially expects 16 kHz input; if your file is 24 kHz you may want to resample.
        mime_type = f"audio/pcm;rate={sr}"

        # configure for text output only
        config = {
            "response_modalities": ["TEXT"],
            "system_instruction": (
                "You are an english transcription system. Your only task is to transcribe the spoken audio into accurate English text. "
                "Do not answer the content, just transcribe exactly what you hear. Consider that the input will be based on the owner's manual of the CUPRA Tavascan 2024. "
                "Always refer to the car as 'CUPRA Tavascan 2024' — correct any misheard or misspelled versions like 'Cupratavaskan', 'Kuprative Vaskin', 'Cooper Tavaskin', 'Cooper to Ask', 'Kupra Tavaskin' etc. "
               # "Normalize similar names to 'CUPRA Tavascan 2024' without exceptions. "
                "Always type the name CUPRA in capital letters."
                "The input you have to transcribe is a question of the user about the CUPRA Tavascan 2024 car. "
            )
        }

        transcript_parts: list[str] = []

        async with self.client.aio.live.connect(model=self.model, config=config) as session:
            # stream raw PCM in small chunks
            while True:
                chunk = wf.readframes(1024)
                if not chunk:
                    break
                # send each chunk as realtime audio
                await session.send_realtime_input(audio=types.Blob(data=chunk, mime_type=mime_type))
                await asyncio.sleep(0.02)  # pacing to avoid buffer issues

            # signal end of audio stream
            await session.send_realtime_input(audio_stream_end=True)

            # collect all text responses
            async for message in session.receive():
                if message.text:
                    transcript_parts.append(message.text)

        wf.close()
        return "".join(transcript_parts)

    async def _start_after_delay(self, event: asyncio.Event, delay: float):
        await asyncio.sleep(delay)
        event.set()

    def record_audio(self, filename: str, duration: int = 5):
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
        sd.wait()
        wf = wave.open(filename, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())
        wf.close()