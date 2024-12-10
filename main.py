from fastapi import FastAPI, WebSocket, BackgroundTasks
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import asyncio
import time

app = FastAPI()

# 1. Custom Middleware (Using Starlette's middleware system)
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        response.headers["X-Process-Time"] = str(end_time - start_time)
        return response

# Add the middleware to FastAPI
app.add_middleware(TimingMiddleware)

# 2. Background Tasks (Starlette feature)
async def write_log(message: str):
    await asyncio.sleep(2)  # Simulate some work
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.get("/task")
async def create_task(background_tasks: BackgroundTasks):
    # This task will run in the background after response is sent
    background_tasks.add_task(write_log, "Task processed")
    return {"message": "Task scheduled"}

# 3. WebSocket Support (Starlette feature)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except:
        await websocket.close()

# 4. Regular REST endpoint (FastAPI/Starlette routing)
@app.get("/hello")
async def read_root():
    return {"message": "Hello World"}

# 5. Using Starlette's Request object directly
@app.get("/info")
async def get_info(request: Request):
    client_host = request.client.host
    headers = request.headers
    return {
        "client_host": client_host,
        "headers": dict(headers)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)