from fastapi import FastAPI, HTTPException, Cookie
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import bot
import logging
import uuid

logging.basicConfig(
    filename="logs.log",  
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"  
)
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Generate unique session ID
def generate_session_id():
    return str(uuid.uuid4())

class QueryInput(BaseModel):
    question: str
    stream: bool = True


@app.post("/ask")
async def handle_question(input: QueryInput, session_id: str = Cookie(default=None)):
    """
    Handle user queries by interacting with the bot function.
    """
    try:
        # Generate session ID if not provided
        if not session_id:
            session_id = generate_session_id()

        logging.info(f"Received question: {input.question} | Session ID: {session_id}")

        if input.stream:
            response = bot(input.question, session_id)
            # response = chain.stream({"question" : input.question, "session_id" : session_id})
            logging.info(f"Streaming response initiated for session ID: {session_id}")
            return StreamingResponse(response, headers={"Set-Cookie": f"session_id={session_id}; Path=/"})
        else:
            # response = chain.invoke({"question" : input.question, "session_id" : session_id})

            response = bot(input.question, session_id)
            logging.info(f"Response generated for session ID: {session_id}")
            return JSONResponse(
                content={"response": response},
                headers={"Set-Cookie": f"session_id={session_id}; Path=/"}
            )
    except Exception as e:
        logging.error(f"Error processing question: {input.question} | Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint to check API status.
    """
    return {"message": "Welcome to the chatbot API!"}
