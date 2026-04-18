from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(client_id + " connected")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id)
        print(client_id + " disconnected")

    async def send_message(self, client_id: str, message: str):
        websocket = self.active_connections[client_id]
        if websocket:
            await websocket.send(message)

    # method to broadcast to all the connected clients

    async def broadcast(self, client_id: str, message: str):
        for connections in self.active_connections.values():
            await connections.send(message)


# Create instance
manager = ConnectionManager()