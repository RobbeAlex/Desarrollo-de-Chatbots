import openai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

client = QdrantClient(host="localhost", port=6333)

def setup_collection():
    client.recreate_collection( 
        collection_name="documentos_empresa",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

def chunk_and_index(text: str, chunk_size: int = 512, overlap: int = 50):
    words = text.split()
    start = 0
    points = []

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        start += chunk_size - overlap
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        vector = response.data[0].embedding

        points.append(PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={"text": chunk}
        ))

    client.upsert(collection_name="documentos_empresa", points=points)

def rag_query(user_query: str): 
    res = openai.embeddings.create(model="text-embedding-3-small", input=user_query)
    q_vec = res.data[0].embedding

    hits = client.search(collection_name="documentos_empresa", query_vector=q_vec, limit=3)
    context = "\\n\\n".join([hit.payload["text"] for hit in hits])
    
    prompt = f"""Responde únicamente basándote en el siguiente contexto. Si no está la información, di que no la conoces.
    
Contexto:
{context}

Pregunta:
{user_query}
 
Respuesta:"""

    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content