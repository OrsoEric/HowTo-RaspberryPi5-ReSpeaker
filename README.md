# HowTo-RaspberryPi5-ReSpeaker

Repository to get ReSpeaker wo record and play audio, and transcribe using whisper on the RaspberryPi5


# Demo Enumerate Microphones

Installation

```bash
uv venv .venv --python 3.12

source .venv/bin/activate

sudo apt install portaudio19-dev

uv pip install sounddevice numpy
```

Execute

```bash
python demo-enumerate-micropphones.py
```

```bash
(.venv) raspi@rpi5-orso-1:~/HowTo-RaspberryPi5-ReSpeaker $ python demo-enumerate-micropphones.py
Available microphone devices:
[0] ReSpeaker 4 Mic Array (UAC1.0):USB Audio (hw:2,0) (channels=6)
```






