from app.db.database import get_connection

#Distance and meaning
#  0.0–0.3 Very similar
#  0.3–0.5 Related
#  0.5–0.7 Weakly related
# 0.7–1.0 Barely related

def retrieve_similar_chunks(query_embedding, user_id, limit=10):
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

    print(format(results))

    cursor.close()
    conn.close()

    # filter by threshold to get the most relevant result
    threshold = 0.9
    filtered = [row[0] for row in results if row[1] < threshold]

    return filtered