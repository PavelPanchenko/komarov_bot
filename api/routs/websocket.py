from typing import List
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse


socket_routs = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@socket_routs.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    print('client_id: ', client_id)
    while True:
        data = await websocket.receive_text()
        print(data)
        # await manager.broadcast(f"Client {client_id}: {data}")