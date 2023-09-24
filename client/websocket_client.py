import asyncio

import websockets


async def send_request(request:str):
    uri = "ws://localhost:8765"  # Replace with your server's address
    async with websockets.connect(uri) as websocket:
        await asyncio.wait_for(websocket.send(request), timeout=240)
        response = await asyncio.wait_for(websocket.recv(), timeout=240)
        return response

# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(send_request())
