import uuid
from psycopg2.extras import execute_values
from app.db.database import get_connection
from app.Contracts.Chunks import Chunk
from typing import List
import nltk
# nltk.download('punkt')

def insert_chunks(chunkList: List[Chunk]):
    print("Inserting chunks")

    connection = get_connection()
    cursor = connection.cursor()

    query_values = []

    for chunk in chunkList:
        chunk_id = str(uuid.uuid4())

        query_values.append((
            chunk_id,
            chunk.document_id,
            chunk.user_id,
            chunk.chunk_index,
            chunk.content,
            chunk.embedding,
            chunk.page_number
        ))

    query = """
        INSERT INTO aip.chunks
        (id, document_id, user_id, chunk_index, content, embedding, page_number)
        VALUES %s
    """

    execute_values(cursor, query, query_values)

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Bulk insert {len(chunkList)} completed!!")