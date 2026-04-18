
from lib2to3.pgen2.parse import Parser
from typing import List

from fastapi import FastAPI, File, UploadFile, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil
import os
from app.db.database import get_connection
from app.helpers.terminalColor import red,green,yellow

from app.services.pdf_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.embedding_service import create_embedding
from app.services.chunk_repository import insert_chunks
from app.services.rag_service import generate_answer
from app.services.retrieval_service import retrieve_similar_chunks
from app.services.document_service import insert_documents_metadata
from app.Contracts.Chunks import Chunk
from app.services.websocket_manager import manager

app = FastAPI(title="DocuMind AI")

origins = [
    "http://localhost:3000",   # Next.js
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.websocket("/ws/{upload_id}")
async def websocket_endpoint(websocket: WebSocket, upload_id: str):
    await manager.connect(upload_id, websocket)
    try:
        while True:
            await websocket.receive_text()   # keep connection alive
    except:
        await manager.disconnect(upload_id)

@app.post("/testws/{upload_id}")
async def testws_endpoint(upload_id: str):
    await manager.send_message(client_id=upload_id, message="test message")
    return {"ok": True}


@app.post("/upload/{upload_id}")
async def upload_file(upload_id:str, file: UploadFile = File(...)):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        await manager.send_message(upload_id, "Upload started")

        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}.pdf"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await manager.send_message(upload_id, "PDF saved")

        data = extract_text_from_pdf(file_path)

        await manager.send_message(upload_id, "Text extracted")

        chunks = chunk_text(data)

        await manager.send_message(upload_id, f"{len(chunks)} chunks created")

        user_id = "4aabd32c-0f5b-4f11-9bcb-a32c5b97c52d"

        document_id = str(uuid.uuid4())

        insert_documents_metadata(
            document_id,
            user_id,
            connection,
            cursor,
            file_path=file_path,
            file_name=file.filename
        )

        await manager.send_message(upload_id, "Document metadata stored")

        batch_size = 300
        no_of_batch = int(len(chunks) / batch_size) + 1

        for i in range(no_of_batch):

            await manager.send_message(upload_id, f"Processing batch {i+1}/{no_of_batch}")

            batch_chunk = chunks[i * batch_size:(i + 1) * batch_size]

            chunks_to_insert = []

            for index, chunk in enumerate(batch_chunk):
                await manager.send_message(upload_id,"creating embedding for chunk {index}/{batch_chunk}")
                embedding = create_embedding(chunk)

                chunks_to_insert.append(
                    Chunk(
                        document_id=document_id,
                        user_id=user_id,
                        chunk_index=index,
                        content=chunk,
                        embedding=embedding
                    )
                )

            insert_chunks(chunks_to_insert, connection, cursor)

        await manager.send_message(upload_id, "All chunks inserted")

        connection.commit()

        await manager.send_message(upload_id, "Document indexed successfully")

        return {
            "message": "Document upload complete",
            "document_id": document_id
        }

    except Exception as e:

        if connection:
            connection.rollback()

        await manager.send_message(upload_id, f"Error: {str(e)}")

        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.post("/ask")
def ask_question(document_ids:List[str], question: str = Body(...)):
    try:
        print("Ask endpoint hit")
        user_id = "4aabd32c-0f5b-4f11-9bcb-a32c5b97c52d"
        enhanced_question = f"Explain clearly: {question.lower().strip()}"
        query_embedding = create_embedding(enhanced_question)
        print(f"{yellow}Embedding created")

        document_id = document_ids[0]
        relevant_chunks = retrieve_similar_chunks(
            document_id,
            query_embedding=query_embedding,
            user_id=user_id,
            question=enhanced_question,
            limit=5
        )
        print(f"{green}Chunks retrieved:", len(relevant_chunks))
        print(format(relevant_chunks))
        answer = 'Empty'
        if len(relevant_chunks) > 0:
            relevant_chunks = "\n\n".join(relevant_chunks)
            answer = generate_answer(question, relevant_chunks)
        print("Answer generated by AI",answer)

        return {"answer": answer}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}


@app.get("/")
def root():
    return {"message": "DocuMind AI is running"}