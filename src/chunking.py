from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv("../.env")

MONGODB_URI = os.getenv("MONGODB_URI")

def create_chunks():
    """
    Load data from the laptops collection in MongoDB Atlas and create chunks.
    """

    loader = MongodbLoader(
        connection_string=MONGODB_URI,
        db_name="laptop_database",
        collection_name="laptops",
        field_names= ["brand", "model", "processor_brand", "processor_name", "processor_gnrtn", "ram_gb", "ram_type", "ssd", "hdd", "os", "os_bit", "graphic_card_gb", "weight", "display_size",  "warranty",  "Touchscreen", "latest_price", "star_rating"]
    )

    # docs = await loader.aload()  
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  
            chunk_overlap=20,  
            length_function=len,
            is_separator_regex=False
        )

    chunks = []
    for page in docs:
        # Splitting the text into smaller chunks
        text = page.page_content
        # split_texts = splitter.split_text(text)
        pieces = splitter.create_documents([text])
        chunks.extend(pieces)  # Add split texts to the chunks

    return chunks

# print("HELLO")
