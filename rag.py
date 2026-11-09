import chromadb
from sentence_transformers import SentenceTransformer


# Create embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
COLLECTION_NAME = "documents"
collection = client.get_or_create_collection(COLLECTION_NAME)


def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def store_document(pages, file_name="Uploaded PDF"):

    global collection

    # Delete old collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    # Create a fresh collection
    collection = client.get_or_create_collection(COLLECTION_NAME)

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    chunk_id = 0

    for page in pages:

        page_number = page["page"]
        page_text = page["text"]

        chunks = split_text(page_text)

        for chunk in chunks:

            ids.append(str(chunk_id))
            documents.append(chunk)
            embeddings.append(
                embedding_model.encode(chunk).tolist()
            )

            metadatas.append({
                "page": page_number,
                "file": file_name
            })

            chunk_id += 1

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_document(query, k=3):

    embedding = embedding_model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k
    )

    documents = results["documents"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]

    return {
        "text": "\n".join(documents),
        "chunks": ids,
        "metadata": metadatas
    }
def has_documents():
    return collection.count() > 0
def clear_documents():
    global collection

    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)