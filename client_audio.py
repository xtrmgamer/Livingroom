import pyaudio
import asyncio
import websockets
import base64

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

async def send_audio(uri):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    async with websockets.connect(uri) as websocket:
        while True:
            data = stream.read(CHUNK)
            encoded_data = base64.b64encode(data)
            await websocket.send(encoded_data)

async def receive_audio(uri):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            decoded_data = base64.b64decode(message)
            stream.write(decoded_data)

async def main():
    uri = "ws://localhost:8765"
    await asyncio.gather(send_audio(uri), receive_audio(uri))

asyncio.get_event_loop().run_until_complete(main())