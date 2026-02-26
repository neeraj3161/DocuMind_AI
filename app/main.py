from fastapi import FastAPI, File, UploadFile, Body
import uuid
import shutil
import os

from app.services.pdf_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.embedding_service import create_embedding
from app.services.chunk_repository import insert_chunk
from app.services.rag_service import generate_answer
from app.services.retrieval_service import retrieve_similar_chunks

app = FastAPI(title="DocuMind AI")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        print("Upload started")

        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}.pdf"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("PDF saved")

        text = extract_text_from_pdf(file_path)
        print("Text extracted")

        chunks = chunk_text(text)
        print("Chunked")

        document_id = str(uuid.uuid4())
        user_id = "4aabd32c-0f5b-4f11-9bcb-a32c5b97c52d"

        for index, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)
            print(f"Embedding created for chunk {index}")

            insert_chunk(
                document_id=document_id,
                user_id=user_id,
                chunk_index=index,
                content=chunk,
                embedding=embedding
            )

        print("All chunks inserted")

        return {"message": "Document upload complete and indexed"}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}


@app.post("/ask")
def ask_question(question: str = Body(...)):
    try:
        print("Ask endpoint hit")

        user_id = "4aabd32c-0f5b-4f11-9bcb-a32c5b97c52d"

        query_embedding = create_embedding(question)
        print("Embedding created")

        relevant_chunks = retrieve_similar_chunks(
            query_embedding=query_embedding,
            user_id=user_id,
            limit=5
        )
        print("Chunks retrieved:", len(relevant_chunks))
        print(format(relevant_chunks))
        answer = generate_answer(question, relevant_chunks)
        print("Answer generated")

        return {"answer": answer}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}


@app.get("/")
def root():
    return {"message": "DocuMind AI isss running"}