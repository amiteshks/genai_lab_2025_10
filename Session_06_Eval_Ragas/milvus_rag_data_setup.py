import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility,
)

# ---------------------------
# 1. Milvus + Embedding Setup
# ---------------------------
COLLECTION_NAME = "employee_policies"

def setup_rag(collection_name=COLLECTION_NAME):
    """
    Create a Milvus collection, connect to it, and insert sample data.
    """

    # Connect to Milvus using alias 'rag_db'
    connections.connect("rag_db", host="localhost", port="19530")

    # Drop collection if exists (for clean setup)
    if utility.has_collection(collection_name, using="rag_db"):
        utility.drop_collection(collection_name, using="rag_db")

    # Define schema
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    ]

    schema = CollectionSchema(fields, description="Employee policy documents")
    collection = Collection(collection_name, schema, using="rag_db")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Sample data
    documents = [
        "Employees are paid bi-weekly via direct deposit.",
        "Vacation accrual starts after 90 days of employment.",
        "Health benefits become active after the first month.",
        "Remote work is allowed up to 3 days per week.",
        "Performance reviews are conducted annually in December."
    ]

    embeddings = model.encode(documents).tolist()

    # Insert data into Milvus
    collection.insert([documents, embeddings])

    # Create index
    collection.create_index(
        "embedding",
        {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
    )
    collection.load()

    print(f"RAG setup complete with {len(documents)} sample records in '{collection_name}'.")
    print( )
    return collection_name


# ---------------------------
# 2. Setup the Data in the Vector DB
# ---------------------------
if __name__ == "__main__":
    setup_rag()
       # Load collection
    collection = Collection(COLLECTION_NAME, using="rag_db")
    collection.load()

    # Query all records (limit = small number to avoid large dumps)
    results = collection.query(expr="id >= 0", output_fields=["id", "content"], limit=10)
    
    print(f"Retrieved {len(results)} records from collection '{COLLECTION_NAME}':\n")
    for r in results:
        print(f"ID: {r['id']} | Content: {r['content']}")

