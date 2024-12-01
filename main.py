import os
from openai import OpenAI
from dotenv import load_dotenv

from db.search import search_book

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

while True:
    query = input("Enter the name of your favorite book (or 'exit' to quit):")
    if query.lower() == 'exit':
        break
    rating = input("Enter your minimum rating (or type 'no preference'):")
    max_pages = input("Enter the maximum pages (or type 'no preference'):")

    description = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": SummaryGenerator}],
                },
                {"role": "user", "content": [{"type": "text", "text": query}]},
            ],
            temperature=0.3,
        )
        .choices[0]
        .message.content
    )

    query_embedding = (
            client.embeddings.create(
                input=description, model="text-embedding-3-small"
            )
            .data[0]
            .embedding
        )

    results = search_book(query_embedding)

    print ("\nTop Results")
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Rating: {result['rating']}\n")
        print(f"Number of Pages: {result['num_pages']}\n")
        print(f"Date Published: {result['date']}\n")
        print(f"Summary: {result['description']}\n")

# things I need to improve
    #  allow for parameter customization with metadata 
    # 