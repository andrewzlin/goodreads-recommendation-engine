from openai import OpenAI
from pinecone import Pinecone
import csv 
import os
from dotenv import load_dotenv

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# index_name = os.getenv("PINECONE_INDEX_NAME")

SummaryGenerator = """
Give me a brief description of this book in three sentences. The first sentence should be about the context the novel was published in. 
The second sentence should be about what type of book this is, and what happens in the book. 
The last sentence should be the main themes it explores. If the query is not a recognizable book, just return "xxx"
"""

with open('books.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        
        embedding = (
            client.embeddings.create(
                input=reader['title']
            )
        )
