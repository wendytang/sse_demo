# Server-Sent Events (SSE) Demo with Starlette

This project demonstrates a real-time messaging system using Server-Sent Events (SSE) implemented with Starlette framework. It shows how to create a simple real-time communication channel from server to clients.

## What This Demonstrates

1. **Server-Sent Events (SSE)**
   - One-way real-time communication from server to clients
   - Automatic reconnection handling
   - Efficient event streaming

2. **Starlette Features**
   - StreamingResponse for SSE
   - Route handling
   - Static file serving
   - ASGI application structure

3. **Asynchronous Programming**
   - Using asyncio.Queue for message distribution
   - Async/await patterns
   - Proper connection handling

## Features

- Real-time message broadcasting
- Multiple client support
- Clean connection handling
- Simple message input interface

## Requirements

```bash
pip install starlette uvicorn
```

## Project Structure

```
fastapi_starlette_demo/
├── sse_example.py    # Main application code
├── sse.html         # Frontend interface
└── README.md        # This file
```

## How to Run

1. Clone or download this repository

2. Install dependencies:
   ```bash
   pip install starlette uvicorn
   ```

3. Run the server:
   ```bash
   python sse_example.py
   ```

4. Open your browser and visit:
   ```
   http://localhost:8000
   ```

5. To test the functionality:
   - Open multiple browser windows/tabs pointing to http://localhost:8000
   - Type a message in any window and click "Send"
   - Observe the message appearing in all windows

## How It Works

1. **Server Side**
   - Creates SSE endpoints for client connections
   - Maintains a set of connected clients using asyncio.Queue
   - Broadcasts messages to all connected clients
   - Handles client disconnections gracefully

2. **Client Side**
   - Connects to SSE endpoint using EventSource API
   - Displays received messages in real-time
   - Sends new messages via POST requests

## Technical Details

### SSE Connection
```python
async def stream_sse(self, request):
    queue = asyncio.Queue()
    self.clients.add(queue)
    
    async def event_generator():
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n".encode('utf-8')
        except asyncio.CancelledError:
            self.clients.remove(queue)
```

### Message Broadcasting
```python
async def broadcast_message(self, message: str):
    for queue in self.clients:
        await queue.put(message)
```

## Key Differences from WebSockets

1. **One-Way Communication**
   - SSE only allows server-to-client communication
   - Simpler than WebSockets for one-way scenarios

2. **HTTP-Based**
   - Uses regular HTTP
   - Better compatibility with firewalls and proxies

3. **Automatic Reconnection**
   - Built-in reconnection handling
   - More resilient to connection drops

## Use Cases

This pattern is particularly useful for:
- Real-time notifications
- Live feed updates
- Status updates
- Event broadcasting
- Any scenario requiring server-to-client push notifications

## License

MIT License