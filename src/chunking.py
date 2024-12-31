from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks():
    loader = MongodbLoader(
        connection_string="mongodb://localhost:27017/",
        db_name="laptop_database",
        collection_name="laptops",
        field_names= ["brand", "model", "processor_brand", "processor_name", "processor_gnrtn", "ram_gb", "ram_type", "ssd", "hdd", "os", "os_bit", "graphic_card_gb", "weight", "display_size",  "warranty",  "Touchscreen", "latest_price", "star_rating"]
    )

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  
            chunk_overlap=20,  
            length_function=len,
            is_separator_regex=False
        )

    chunks = []
    for page in docs:
        text = page.page_content
        chunks.append(text)

    return chunks