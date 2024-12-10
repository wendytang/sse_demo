from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response, HTMLResponse, FileResponse, StreamingResponse
from starlette.background import BackgroundTask
from starlette.staticfiles import StaticFiles
import asyncio
import json
import typing
from datetime import datetime
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

class SseServerTransport:
    def __init__(self, endpoint_path: str):
        self.endpoint_path = endpoint_path
        self.clients: typing.Set[asyncio.Queue] = set()
    
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
        
        return StreamingResponse(
            event_generator(),
            media_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            }
        )
    
    async def broadcast_message(self, message: str):
        for queue in self.clients:
            await queue.put(message)
    
    async def handle_post_message(self, request):
        body = await request.body()
        message = body.decode()
        await self.broadcast_message(message)
        return Response(status_code=200)

# Create SSE transport
sse = SseServerTransport("/messages")

async def handle_sse(request):
    return await sse.stream_sse(request)

async def handle_messages(request):
    return await sse.handle_post_message(request)

# Root handler to serve the HTML file
async def homepage(request):
    return FileResponse(os.path.join(current_dir, 'sse.html'))

# Define routes
routes = [
    Route("/", endpoint=homepage),
    Route("/sse", endpoint=handle_sse),
    Route("/messages", endpoint=handle_messages, methods=["POST"])
]

# Create application
app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    print(f"Server running. Visit http://localhost:8000 to see the SSE demo")
    uvicorn.run(app, host="0.0.0.0", port=8000)