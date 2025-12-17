from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()
active_connections: List[WebSocket] = []

async def connect(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    await broadcast("A new user joined the chat")

async def disconnect(ws: WebSocket):
    active_connections.remove(ws)
    await broadcast("A user left the chat")

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await connect(ws)
    try:
        while True:
            message = await ws.receive_text()
            await broadcast(f"{message}")
    except WebSocketDisconnect:
        await disconnect(ws)
    except Exception as e:
        await disconnect(ws)


