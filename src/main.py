# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse, StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from chatbot import bot 
# import uuid
# import logging

# logging.basicConfig(
#     filename="logs.log",  
#     level=logging.INFO,  
#     format="%(asctime)s - %(levelname)s - %(message)s"  
# )

# # Initialize FastAPI app
# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# class QueryInput(BaseModel):
#     question: str
#     stream: bool = False

# def generate_session_id():
#     return str(uuid.uuid4())

# @app.post("/ask")
# async def handle_question(input: QueryInput):
#     """
#     Handle user queries by interacting with the bot function.
#     """
#     try:
#         session_id = generate_session_id()
#         logging.info(f"Received question: {input.question} | Session ID: {session_id}")

#         if input.stream:
#             response = bot(input.question, session_id)
#             logging.info(f"Streaming response initiated for session ID: {session_id}")
#             return StreamingResponse(response)  
#         else:
#             response = bot(input.question, session_id)
#             logging.info(f"Response generated for session ID: {session_id}")
#             return JSONResponse(content={"response": response, "session_id": session_id})
#     except Exception as e:
#         logging.error(f"Error processing question: {input.question} | Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# async def root():
#     """
#     Root endpoint to check API status.
#     """
#     logging.info("Root endpoint accessed")
#     return {"message": "Welcome to the Laptop Suggestion Chatbot API!"}

from fastapi import FastAPI, HTTPException, Cookie
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.chatbot import bot
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
)

# Generate unique session ID
def generate_session_id():
    return str(uuid.uuid4())

class QueryInput(BaseModel):
    question: str
    stream: bool = False

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
            logging.info(f"Streaming response initiated for session ID: {session_id}")
            return StreamingResponse(response, headers={"Set-Cookie": f"session_id={session_id}; Path=/"})
        else:
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
