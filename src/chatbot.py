from embeddings import retrieve_chunks
from chat_history import save_chat, fetch_chat
from openai import OpenAI
from dotenv import load_dotenv
import os, logging
import asyncio

load_dotenv("../.env")


PROMPT = """
    You are a chatbot specializing in laptop recommendations based on user usecases and requirements. You need to give the response in a very structured format. Mention the name of the specs and its value properly. Use Pakistani Rupees PKR as the unit of price instead of INR. Keep the conversation engaging. Make the conversion as engaging as possible for instance if I user just tell you the use case without mentioning any specific brand or price range, ask the user about these things and other that can help you give better response in terms of laptop recommendation. And the laptops that you recommend must be from the ones stored in the chromadb database.You must response in the language that user has asked question in. If a user asks a question other than laptops just simply say "I'm sorry I can't respond to that. You can ask me about laptop recommendations." but if they ask whether you can respond in a particular language make sure to reply to them with a yes in that language. If a users asks you about a laptop that is in your database, you can give him the deatils of it and for which use case it will be best. However if a user asks about a certain laptop or brand that is not in your database you can reply "I don't have information about this particular model/brand in my database".
    You will recommend laptops from here {data}
    This is the question : {question}
    
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


