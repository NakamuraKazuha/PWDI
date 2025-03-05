import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):  
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")
            # Broadcast message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Prevent echo to sender
                    await client.send(json.dumps(data))
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    print("Starting WebSocket server on ws://localhost:6789")
    async with websockets.serve(handler, "0.0.0.0", 6789):
        await asyncio.Future()  # Run forever

asyncio.run(main())
