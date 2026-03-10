import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import sys

# --- SETTINGS ---
MODEL_SIZE = "large-v3-turbo"
SAMPLE_RATE = 16000    # Whisper requirement
CHUNK_SIZE = 1024      # Small blocks of audio
DEVICE = "cpu"         # Change to "cuda" on Linux/AMD with ROCm
COMPUTE_TYPE = "int8"  # Use "float16" on Linux/GPU

# This queue stores audio chunks from the mic
audio_queue = queue.Queue()

print(f"Loading {MODEL_SIZE}...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

def callback(indata, frames, time, status):
    """This is called by sounddevice for every audio chunk."""
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata.copy())

def process_audio():
    print("\n🎤 Listening... (Press Ctrl+C to stop)")
    
    # We aggregate audio here until we have enough to transcribe
    audio_buffer = []
    
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=CHUNK_SIZE):
            while True:
                # Get audio from the queue
                chunk = audio_queue.get()
                audio_buffer.append(chunk)

                # Transcribe every ~2-3 seconds of audio, or use VAD logic
                # For a true VAD "trigger," you'd check volume levels here
                if len(audio_buffer) > (SAMPLE_RATE / CHUNK_SIZE) * 3: 
                    full_audio = np.concatenate(audio_buffer).flatten()
                    
                    # VAD FILTER: This is the 'Whisper way' to handle silence
                    segments, _ = model.transcribe(
                        full_audio, 
                        beam_size=1, 
                        language="en",
                        vad_filter=True,
                        vad_parameters=dict(min_silence_duration_ms=500)
                    )

                    for segment in segments:
                        if segment.text.strip():
                            print(f"💬 {segment.text.strip()}")
                    
                    # Clear buffer after transcribing
                    audio_buffer = []

    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    process_audio()