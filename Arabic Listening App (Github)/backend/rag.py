import chromadb

# Setup Chroma in-memory
client = chromadb.Client()

# Create collection
collection = client.create_collection("arabic-listening-comprehension")

# Optional: Add documents to the collection
# Replace these paths with actual file paths or remove this block if not needed
try:
    # Use actual paths to your transcript files
    with open('./transcripts/sample_transcript1.txt', 'r') as f1, open('./transcripts/sample_transcript2.txt', 'r') as f2:
        doc1 = f1.read()
        doc2 = f2.read()

    # Add documents to ChromaDB
    collection.add(
        documents=[doc1, doc2],
        metadatas=[
            {"source": "sample_transcript1.txt"},
            {"source": "sample_transcript2.txt"}
        ],
        ids=["doc1", "doc2"],
    )
    print("Documents added to ChromaDB successfully!")
except FileNotFoundError:
    print("No documents found. Skipping document addition to ChromaDB.")

# Query/search 2 most similar results
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
)
print(results)