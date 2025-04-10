'''

Handle One Shot Interrupt Scanning with device

Websocket for dynamic updates to front end with new messages

Websocket Source: https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
'''

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Example</title>
</head>
<body>
    <h1>Device Messages</h1>
    <div id="messages"></div>
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function(event) {
            const messagesDiv = document.getElementById("messages");
            messagesDiv.innerHTML += `<p>${event.data}</p>`;
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Simulate receiving messages from the device
        message = "New message from device"
        await websocket.send_text(message)
