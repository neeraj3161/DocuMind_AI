from app.db.database import get_connection

def retrieve_similar_chunks(query_embedding, user_id, limit=5):
    connection = get_connection()
    cursor = connection.cursor()
    query_embedding = "[" + ",".join(map(str, query_embedding)) + "]"

    cursor.execute("""SELECT content
                   FROM aip.chunks
                   WHERE user_id = %s
                   ORDER BY embedding <-> %s::vector
                   LIMIT %s""", (user_id, query_embedding, limit)
                   )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return [row[0] for row in results]