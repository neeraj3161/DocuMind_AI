import uuid
from psycopg2.extras import execute_values
from app.db.database import get_connection
from app.Contracts.Chunks import Chunk
from typing import List
import sys
import nltk
# nltk.download('punkt')
from app.helpers.terminalColor import yellow, green, red

def insert_chunks(chunkList: List[Chunk], connection, cursor):
    try:
        print(f"{yellow}Inserting chunks")

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
                chunk.page_number,
                chunk.content
            ))

        query = """
                INSERT INTO aip.chunks
                (id, document_id, user_id, chunk_index, content, embedding, page_number, content_tsv)
                VALUES %s
            """

        execute_values(cursor, query, query_values, template="(%s,%s,%s,%s,%s,%s,%s,to_tsvector('english',%s))")

        print(f"{green}Bulk insert {len(chunkList)} completed!!")
    except Exception as e:
        print(f"{red}[ERROR]: While inserting chunk {e} \n Rolling back")
        connection.rollback()