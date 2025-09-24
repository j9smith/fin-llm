from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend_app.services.chatbot import chat_logic
from backend_app.services.auth.auth_routes import auth_router
import json

app = FastAPI()

app.include_router(auth_router)

allowed_origins = [
    "http://localhost:3000",  # Development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specify the frontend's origin, here we have dev and prod
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (e.g., GET, POST, OPTIONS)
    allow_headers=["*"],  # Allows all headers (e.g., Content-Type)
)
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.post("/chat") # Triggered when handleUserMessage() is called in script.js. The user message is POSTed to this route.
async def chat(request: Request):
    chat_history = await request.json()  # Asynchronously read the request body, include chat history
    if not chat_history:
        return JSONResponse({"error": "Message is required"}, status_code=status.HTTP_400_BAD_REQUEST)

    response = chat_logic.get_chatgpt_stream(chat_history)
 
    async def generate_stream():
        print("Generating stream ...")
        async for chunk in response:
            if isinstance(chunk, dict):  # If the chunk is a dictionary (i.e., the result of a tool call), convert the chunk into a JSON string and pass it to the frontend.
                yield json.dumps(chunk)
            else:
                yield chunk
    
    return StreamingResponse(generate_stream(), media_type="text/event-stream")