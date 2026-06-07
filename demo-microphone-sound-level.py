import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 44100
BLOCK_DURATION = 0.2  # seconds


"""
uv venv .venv --python 3.12

source .venv/bin/activate

sudo apt install portaudio19-dev

uv pip install sounddevice numpy

python demo-microphone-sound-level.py


"""


def list_microphones():
    devices = sd.query_devices()

    print("Available microphone devices:")
    mic_indices = []

    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            mic_indices.append(idx)

            print(
                f"[{idx}] "
                f"{dev['name']} "
                f"(channels={dev['max_input_channels']})"
            )

    return mic_indices


def rms_to_dbfs(rms):
    if rms <= 0:
        return -120.0

    return 20 * np.log10(rms)


def measure_microphone(device_index):
    block_size = int(SAMPLE_RATE * BLOCK_DURATION)

    print(f"\nMonitoring device {device_index}")
    print("Press Ctrl+C to stop\n")

    while True:
        audio = sd.rec(
            frames=block_size,
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32',
            device=device_index
        )

        sd.wait()

        rms = np.sqrt(np.mean(audio**2))
        dbfs = rms_to_dbfs(rms)

        print(f"Level: {dbfs:7.2f} dBFS")


def main():
    microphones = list_microphones()

    if not microphones:
        print("No microphones found")
        return

    # Automatically select first microphone
    selected_mic = microphones[0]

    measure_microphone(selected_mic)


if __name__ == "__main__":
    main()