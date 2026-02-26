import uuid
from app.db.database import get_connection

def insert_chunk(document_id, user_id, chunk_index, content, embedding):
    connection = get_connection()
    cursor = connection.cursor()

    chunk_id = str(uuid.uuid4())

    cursor.execute("""
    INSERT INTO aip.chunks (id, user_id, chunk_index, content, embedding)
    VALUES (%s, %s, %s, %s, %s)
    """, (chunk_id, user_id, chunk_index, content, embedding))
    connection.commit()
    cursor.close()
    connection.close()