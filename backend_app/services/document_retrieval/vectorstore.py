# vectorstore.py
import os 
import fitz
import json
import backend_app.services.chatbot.functions as functions

client = None
collection = None
embedding_model = None
filings_directory = "./filings/"
persistent_directory = "./vectordb/"

def initialise():
    print(f"Initialising vectordb module ...")
    import chromadb
    from sentence_transformers import SentenceTransformer

    global client, collection, embedding_model

    if embedding_model is None: 
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    if not os.path.exists(persistent_directory):
        os.makedirs(persistent_directory)

    if client is None:
        client = chromadb.PersistentClient(settings=chromadb.Settings(persist_directory=persistent_directory))
        collection = client.get_or_create_collection(name="filings")

    if collection is None: 
        print("Failed to create or retrieve a collection")

def check_existing_data():
    initialise()

    existing_ids = collection.get()["ids"]
    if existing_ids:
        print("Existing data found in collection:", existing_ids)
        return True  # Return True if data exists
    else:
        print("No existing data found in collection. New data will be added.")
        return False  # Return False if no data exists

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    print(f"Extracted text length from {pdf_path}: {len(text)}")
    return text 

def generate_chunks(pdf_path):
    print(f"Extracting text from {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    text_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    print(f"Chunks created: {len(text_chunks)}")

    return text_chunks

def add_filings_to_chromadb():
    initialise()

    existing_ids = collection.get()["ids"]
    
    if existing_ids and len(existing_ids) > 0:
        print("Data already exists. Skipping processing.")
        return  

    # Process each PDF in the directory

    for filename in os.listdir(filings_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(filings_directory, filename)

            text_chunks = generate_chunks(pdf_path)            

            print("Generating embeddings")
            embeddings = embedding_model.encode(text_chunks)

            print("Adding chunks and embeddings to collection")

            # Given filename tsla_20231231.pdf:
            filename_ticker = filename[:4] # Selects the first 4 letters in filename [i.e., tsla]
            filename_date = filename[5:-4] # Skips the first 5 letters, and then takes all letters except the final 4 [i.e., 20231231]

            for idx, chunk in enumerate(text_chunks):
                try: 
                    collection.add(
                        documents=[chunk], 
                        ids=[f"{filename}_doc_{idx}"],  # Unique ID for each document
                        embeddings=[embeddings[idx]],
                        metadatas=[{"filename" : filename, "ticker" : filename_ticker, "date_yyyymmdd" : filename_date}]
                    )
                except Exception as e: 
                    print(f"Error adding document {idx} from {filename}: {e}")


def retrieve_relevant_chunks(query, top_k=3):
    initialise()

    query_embedding = embedding_model.encode([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results = top_k
    )
    
    return results["documents"][0]

def retrieve_filings(arguments):
    arguments = json.loads(arguments)
    ticker = arguments.get("ticker")
    keywords = arguments.get("keywords")
    initialise()  # Ensure the vector store is initialized

    query_text = " ".join(keywords)
    conditional_clause = {"ticker": ticker}

    query_embedding = embedding_model.encode([query_text])[0]

    results = collection.query(
        where=conditional_clause, 
        query_embeddings=[query_embedding],
        n_results=5  # Number of chunks to return
    )

    documents = results["documents"][0]
    # Combine into one string for tool output message to api, could possibly amend this in future to pass a key:value pair of documentname:content
    documents = ''.join(documents)
    documents = functions.create_json_response(response_model_content=documents)
    return documents