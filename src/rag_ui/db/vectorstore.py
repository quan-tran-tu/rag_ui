from pymilvus import MilvusClient

from rag_ui.data.preprocessing import to_chunks
from rag_ui.inference.ollama_client import ollama_embed_response

MILVUS_METRIC_TYPE = "COSINE"

def init_milvus_client():
    # temporary hard-code endpoint
    milvus_endpoint = "./src/rag_ui/db/milvus.db"

    client = MilvusClient(milvus_endpoint)
    return client

def check_collection(client, collection_name: str = None, drop_old: bool = True):
    """Check if the collection existed in the vector database"""
    if client.has_collection(collection_name) and drop_old:
        client.drop_collection(collection_name)
    if client.has_collection(collection_name):
        raise RuntimeError(
            f"Collection {collection_name} already exists. Set drop_old=True to create a new one instead."
        )
        
def create_collection(client, collection_name: str, dim: int):
    """Create the collection in the vector database if the collection doesn't exist"""
    check_collection(client, collection_name)
    return client.create_collection(
        collection_name=collection_name,
        dimension=dim,
        metric_type=MILVUS_METRIC_TYPE,
        consistency_level="Strong",
        auto_id=True,
    )

def get_search_results(client, collection_name: str, query_vector, output_fields):
    """Get the search result with the output fields list"""
    search_res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=3,
        search_params={"metric_type": MILVUS_METRIC_TYPE, "params": {}},  # Inner product distance
        output_fields=output_fields, # A list of str represents output fields
    )
    return search_res

def insert(client, text, file_path, collection_name):
    """Insert the embeddings gotten from text chunks with the correspond text and file path"""
    data = []
    chunks = to_chunks(text)
    embeddings = ollama_embed_response("llama3.2", chunks)
    for chunk, embedding in zip(chunks, embeddings):
        data.append({"vector": embedding, "text": chunk, "file_path": file_path})
    try: 
        mr = client.insert(collection_name=collection_name, data=data)
        return f"Total number of chunks inserted: {mr['insert_count']}"
    except Exception as e:
        return f"Error inserting data: {e}"
