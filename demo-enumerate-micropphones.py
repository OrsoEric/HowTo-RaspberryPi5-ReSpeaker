

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
from typing import List, Dict, Any, Tuple


class lib_sounddevice:
    from sounddevice import query_devices, InputStream


COMMON_SAMPLE_RATES = [
    8000,
    16000,
    22050,
    32000,
    44100,
    48000,
]


def list_microphones() -> List[int]:
    devices = lib_sounddevice.query_devices()

    print("Available microphone devices:")
    mic_indices = []

    for idx, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            mic_indices.append(idx)
            print(f"[{idx}] {dev['name']} (channels={dev['max_input_channels']})")

    return mic_indices


def test_stream(device_index: int, channels: int, samplerate: int) -> bool:
    """Try opening + closing a stream."""
    try:
        with lib_sounddevice.InputStream(
            device=device_index,
            channels=channels,
            samplerate=samplerate,
        ):
            return True
    except Exception:
        return False


def probe_device(device_index: int) -> Dict[str, Any]:
    """
    Test all (channels × sample_rates) combinations for one device.
    Returns full compatibility map.
    """
    dev = lib_sounddevice.query_devices(device_index)
    max_channels = dev["max_input_channels"]

    print(f"\nProbing device {device_index}: {dev['name']}")
    print(f"Max input channels: {max_channels}")

    supported: List[Tuple[int, int]] = []

    for ch in range(1, max_channels + 1):
        for sr in COMMON_SAMPLE_RATES:
            if test_stream(device_index, ch, sr):
                print(f"  ✓ channels={ch}, samplerate={sr}")
                supported.append((ch, sr))
            else:
                print(f"  ✗ channels={ch}, samplerate={sr}")

    return {
        "device_index": device_index,
        "name": dev["name"],
        "max_channels": max_channels,
        "supported": supported,
    }

def main():
    mic_indices = list_microphones()

    if not mic_indices:
        print("No microphones found")
        return

    print("\nTesting compatibility matrix...\n")

    results = []

    for idx in mic_indices:
        results.append(probe_device(idx))

    print("\n\n===== FULL SUMMARY =====")

    for r in results:
        print(f"\nDevice: {r['name']}")
        print(f"Supported combinations ({len(r['supported'])}):")
        for ch, sr in r["supported"]:
            print(f"  - channels={ch}, samplerate={sr}")


if __name__ == "__main__":
    main()