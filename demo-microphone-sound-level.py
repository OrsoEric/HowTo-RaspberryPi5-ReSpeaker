"""
uv venv .venv --python 3.12

source .venv/bin/activate

sudo apt install portaudio19-dev

uv pip install sounddevice numpy

python demo-microphone-sound-level.py


"""
import sounddevice as sd
import numpy as np
import wave

# ===== CONFIG =====
CHANNELS = 1
SAMPLERATE = 16000
DURATION = 3
OUTPUT_FILE = "test.wav"
# ===================

def rms(x):
    return np.sqrt(np.mean(x**2))

def dbfs(rms_val):
    return 20 * np.log10(rms_val + 1e-12)

def save_wav(filename, data, samplerate):
    """Save float32 audio [-1, 1] to WAV using built-in wave module."""
    # convert to int16 PCM
    audio_int16 = (data * 32767).astype(np.int16)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 2 bytes = int16
        wf.setframerate(samplerate)
        wf.writeframes(audio_int16.tobytes())

def main():
    print(f"Recording {DURATION} seconds...")

    audio = sd.rec(
        int(DURATION * SAMPLERATE),
        samplerate=SAMPLERATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()

    # Save audio
    save_wav(OUTPUT_FILE, audio, SAMPLERATE)

    # Convert to mono for analysis
    mono = audio.mean(axis=1)

    peak_to_peak = np.max(mono) - np.min(mono)
    rms_val = rms(mono)
    avg_abs = np.mean(np.abs(mono))
    level_dbfs = dbfs(rms_val)

    print("\n--- Signal Statistics ---")
    print(f"Peak-to-Peak: {peak_to_peak:.6f}")
    print(f"RMS:          {rms_val:.6f}")
    print(f"Avg Abs:      {avg_abs:.6f}")
    print(f"Level dBFS:   {level_dbfs:.2f} dB")

    print(f"\nSaved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()