import sys
import json
import queue
from threading import Timer
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from pynput import keyboard
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000
EXTRA_TIME = 0.5  

model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, SAMPLE_RATE)
audio_queue = queue.Queue()
is_recording = False
is_padding = False

def process_audio():
    global is_padding
    is_padding = False

    result = json.loads(rec.FinalResult())
    text = result.get("text", "").strip()
    if text:
        print(text)
        sys.stdout.flush()
    else:
        print("⚠️ No speech recognized.", file=sys.stderr)
    rec.Reset()

def audio_callback(indata, frames, time_info, status):
    if is_recording or is_padding:
        data = bytes(indata)
        rec.AcceptWaveform(data)  

def on_press(key):
    global is_recording, is_padding
    if key == keyboard.Key.caps_lock:
        if not is_recording:
            is_recording = True
            is_padding = False
            print("🎙️ Recording...", file=sys.stderr)
        else:
            is_recording = False
            is_padding = True
            print(f"⏳ Padding {EXTRA_TIME}s...", file=sys.stderr)
            Timer(EXTRA_TIME, process_audio).start()

with sd.RawInputStream(
    samplerate=SAMPLE_RATE, 
    blocksize=2000,  
    dtype='int16', 
    channels=1, 
    callback=audio_callback
    ):
    print("System Ready. Press CAPS LOCK to toggle recording.", file=sys.stderr)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()