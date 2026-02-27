from app.db.database import get_connection

def retrieve_similar_chunks(query_embedding, user_id, limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    cursor.execute("""
        SELECT content, embedding <-> %s::vector AS distance
        FROM aip.chunks
        WHERE user_id = %s
        ORDER BY distance
        LIMIT %s
    """, (embedding_str, user_id, limit))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # filter by threshold to get the most relevant result
    threshold = 0.6
    filtered = [row[0] for row in results if row[1] < threshold]

    return filtered