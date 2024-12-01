from openai import OpenAI
from pinecone import Pinecone
import csv 
import os
from dotenv import load_dotenv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("PINECONE_INDEX_NAME")
index = pinecone.Index(index_name)

SummaryGenerator = """
Give me a brief description of this book in three sentences. In your description, cover the genre of the novel, what the novel is about, what themes
the novel explores, and the general tone of the novel. If the query is not a recognizable book, just return "xxx"

Query: Norwegian Wood
Norwegian Wood by Haruki Murakami is a literary fiction novel set in 1960s Tokyo, blending elements of romance, coming-of-age, 
and psychological drama. It follows Toru Watanabe, a young university student, as he navigates complex relationships with two 
women—Naoko, a fragile woman dealing with grief, and Midori, a lively and independent character. 
The novel explores themes of love, loss, mental illness, and the search for identity, with a melancholic and introspective tone 
that captures the emotional complexities of youth and the impact of personal trauma.

Query: Boink oink beep beep
xxx
"""

with open('books.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        
        
        description = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [{"type": "text", "text": row['title']}]},],
            temperature=0.3,
        )
        .choices[0]
        .message.content
        )

        embedding = (
            client.embeddings.create(
                input=description, model="text-embedding-3-small"
            )
            .data[0]
            .embedding
        )

        index.upsert(
            [
                (
                    row['title'],
                    embedding,
                    {"title": row['title'], "author": row["authors"], "rating":row["average_rating"], "date":row["publication_date"], "num_pages":row["pages"], "description":description})
            ]
        )
        
