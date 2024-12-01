from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

def search_book(query_embedding, max_res=1, threshold=0.4, rating=0, num_pages=5000):
    # filter = {
    #     "num_pages" : {"$lte": num_pages},
    #     "rating":{"gte":rating},
    # }

    # if index_name not in pinecone.list_indexes.names():
    #     print ("Warning: Index not loaded")
    #     return []
    index = pinecone.Index(index_name)
    
    raw_results = index.query(
        vector = query_embedding,
        top_k=max_res,
        include_metadata=True,
        # filter=filter
    )
    
    filtered_results = [
        match["metadata"]
        for match in raw_results["matches"]
        if match["score"] >= threshold 
        # and match["metadata"].get("title") != query_title
    ]

    return filtered_results