# from openai import OpenAI
# import os
#
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# def create_embedding(text):
#     response = client.embeddings.create(model="text-embedding-3-small", input=text)
#     print('response from OpenAI: {}'.format(response))
#     return response.data[0].embedding


from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(text: str):
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()