from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import logging
load_dotenv("../.env")

logging.basicConfig(
    filename="logs.log",  
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"  
)
def store_chunks(chunks):
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002'
    )

    vectorstore = Chroma(
        persist_directory="../chromadb",  
        embedding_function=embeddings,
        collection_name="laptop_collection"  
    )

    print("Adding documents to vectorstore...")

    # Chroma.add_documents(vectorstore, chunks)
    Chroma.add_texts(vectorstore, chunks)

    print("Documents added to vectorstore!")

def retrieve_chunks(question, top_k=2):
    embeddings = OpenAIEmbeddings(
        model='text-embedding-ada-002'
    )

    vectorstore = Chroma(
        persist_directory="../chromadb",  
        embedding_function=embeddings,
        collection_name="laptop_collection"
    )

    print("Retrieving documents...")
    relevant_docs = vectorstore.similarity_search(question, top_k)
    print("Documents Retrieved")
    return relevant_docs
    

