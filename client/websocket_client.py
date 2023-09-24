import asyncio

import websockets


async def send_request(request:str):
    uri = "ws://localhost:8765"  # Replace with your server's address
    async with websockets.connect(uri) as websocket:
        await websocket.send(request)
        response = await websocket.recv()
        return response

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_request())
