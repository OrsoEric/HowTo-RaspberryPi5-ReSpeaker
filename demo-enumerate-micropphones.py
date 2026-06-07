

"""
uv venv .venv --python 3.12

source .venv/bin/activate

sudo apt install portaudio19-dev

python demo-enumerate-micropphones.py

uv pip install sounddevice numpy

(.venv) raspi@rpi5-orso-1:~/HowTo-RaspberryPi5-ReSpeaker $ python demo-enumerate-micropphones.py
Available microphone devices:
[0] ReSpeaker 4 Mic Array (UAC1.0):USB Audio (hw:2,0) (channels=6)


"""

import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 44100
BLOCK_DURATION = 0.2  # seconds


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

def main():
    microphones = list_microphones()

    if not microphones:
        print("No microphones found")
        return

if __name__ == "__main__":
    main()