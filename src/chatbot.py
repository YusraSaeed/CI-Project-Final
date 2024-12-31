from src.embeddings import retrieve_chunks
from src.chat_history import save_chat, fetch_chat
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("../.env")


PROMPT = """
    You are a chatbot specializing in laptop recommendations based on user usecases and requirements. You need to give the response in a very structured format. Mention the name of the specs and its value properly. Use Pakistani Rupees PKR as the unit of price instead of INR. Keep the conversation engaging. Make the conversion as engaging as possible for instance if I user just tell you the use case without mentioning any specific brand or price range, ask the user about these things and other that can help you give better response in terms of laptop recommendation. And the laptops that you recommend must be from the ones stored in the chromadb database.You must response in the language that user has asked question in. If a user asks a question other than laptop recommendation just simply say "I'm sorry I can't respond to that. You can ask me about laptop recommendations."but if they ask whether you can respond in a particular language make sure to reply to them with a yes in that language."
"""

# Helper to call OpenAI
def call_open_ai(messages):
    client = OpenAI()
    response = client.chat.completions.create(
        temperature=0.7,  
        model="gpt-4o-mini",   
        messages=messages
    )
    return response.choices[0].message.content

# Step 1: Retrieve and format context
def retrieve_context(question):
    docs = retrieve_chunks(question)
    text = [doc.page_content for doc in docs]
    combined_text = " ".join(text)
    return combined_text

# Step 2: Prepare messages
def prepare_messages(question, user_id, combined_text):
    history = fetch_chat(user_id)
    clean_history = [
        {"role": item["role"], "content": item["content"]} for item in history
    ]

    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "system", "content": f"Context: {combined_text}"},
    ]
    messages.extend(clean_history)
    messages.append({"role": "user", "content": question})
    return messages

# Step 3: Generate chatbot response
def bot(question, user_id):
    # Retrieve context
    combined_text = retrieve_context(question)
    
    # Prepare messages
    messages = prepare_messages(question, user_id, combined_text)

    # Save user input to chat history
    user_chat = {
        "user_id": user_id,
        "role": "user",
        "content": question
    }
    save_chat(user_chat)

    # Generate response
    response = call_open_ai(messages)

    # Save chatbot response to chat history
    ai_chat = {
        "user_id": user_id,
        "role": "assistant",
        "content": response
    }
    save_chat(ai_chat)

    return response




# import os
# from langchain.tools import Tool
# from langchain_community.chat_models import ChatOpenAI
# from langchain.agents import initialize_agent
# from chat_history import save_chat, fetch_chat  # Assuming these are in your project
# from embeddings import retrieve_chunks  # Assuming this is in your project
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv("../.env")

# # Define the tool
# def retrieve_chunks_tool(question: str):
#     """
#     Tool wrapper for the retrieve_chunks function.
#     """
#     return retrieve_chunks(question)

# chunk_retrieval_tool = Tool(
#     name="Retrieve Laptops",
#     description="Fetches relevant laptop details from the database based on the question.",
#     func=retrieve_chunks_tool
# )

# tools = [chunk_retrieval_tool]

# # Define the chatbot's prompt
# PROMPT = """
#     You are a chatbot specializing in laptop recommendations based on user usecases and requirements. You need to give the response in a very structured format. Mention the name of the specs and its value properly. Use Pakistani Rupees PKR as the unit of price instead of INR.  Make the conversion as engaging as possible for instance if I user just tell you the use case without mentioning any specific brand or price range, ask the user about these things and other that can help you give better response in terms of laptop recommendation. Use the providedto retrieve laptop details from a database.
# Only use tools when necessary i.e. when it time to make the recommendation after asking about price and features.You must response in the language that user has asked question in. If a user asks a question other than laptop recommendation just simply say "I'm sorry I can't respond to that. You can ask me about laptop recommendations."but if they ask whether you can respond in a particular language make sure to reply to them with a yes in that language."
# """
# PROMPT = """
#     You are a chatbot specializing in laptop recommendations based on user usecases and requirements.
# """

# # Define the bot function
# def bot(question, user_id):
#     """
#     Handle user questions by leveraging tools and saving chat history.
#     """
#     # Initialize OpenAI LLM
#     llm = ChatOpenAI(
#         model="gpt-4o-mini", 
#         temperature=0.7,
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

#     # Initialize the agent
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent_type="zero-shot-react-description",
#         handle_parsing_errors=True 
#     )

#     # Retrieve chat history
#     history = fetch_chat(user_id)
#     clean_history = [
#         {"role": item["role"], "content": item["content"]} for item in history
#     ]

#     # Add system message and user query
#     messages = [
#         {"role": "system", "content": PROMPT},
#         *clean_history,
#         {"role": "user", "content": question}
#     ]

#     # Save user query to chat history
#     user_chat = {
#         "user_id": user_id,
#         "role": "user",
#         "content": question
#     }
#     save_chat(user_chat)

#     # Run agent with tool calls
#     try:
#         response = agent.run(input=question)
#     except Exception as e:
#         response = f"I'm sorry, I encountered an error while processing your request: {str(e)}"

#     # Save chatbot response to chat history
#     ai_chat = {
#         "user_id": user_id,
#         "role": "assistant",
#         "content": response
#     }
#     save_chat(ai_chat)

#     return response

