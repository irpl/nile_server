from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from typing import List
import socket

TS_HOST = "127.0.0.1"
TS_PORT = 65432

app = FastAPI()

class ConnectionManager:
  def __init__(self):
    self.connections: List[WebSocket] = []

  async def connect(self, websocket: WebSocket):
    await websocket.accept()
    self.connections.append(websocket)

  # todo remove websocket from connections list on close
  async def disconnect(self, websocket: WebSocket):
    self.connections.remove(websocket)

  async def broadcast(self, data: dict):
    for connection in self.connections:
      await connection.send_json(data)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await manager.connect(websocket)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((TS_HOST, TS_PORT))
  try:
    while True:
      data = await websocket.receive_text()
      # client.send(bytes.fromhex(data))
      client.send(data.encode())
      
  except WebSocketDisconnect:
    await manager.disconnect(websocket)
    client.close()