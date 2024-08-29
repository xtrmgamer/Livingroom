import asyncio
import websockets
import cv2
import base64
import numpy as np

async def send_video(uri):
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            await websocket.send(jpg_as_text)

async def receive_video(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            jpg_original = base64.b64decode(message)
            np_array = np.frombuffer(jpg_original, dtype=np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

async def main():
    uri = "ws://localhost:8765"
    await asyncio.gather(send_video(uri), receive_video(uri))

asyncio.get_event_loop().run_until_complete(main())