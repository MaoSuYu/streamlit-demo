import asyncio
import json

import websockets


async def websocket_example(text):
    uri = "ws://127.0.0.1:10000/webapi/chat?satoken=93aee8f9-6f14-45f9-9da1-b3ccfb36deb9"  # Replace with the actual WebSocket URI
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send(json.dumps({
            "chat_id": "1790335694417227776",
            "message": text
        }))
        # Continuously receive messages
        while True:
            response = await websocket.recv()
            yield json.loads(response)['data']['message']