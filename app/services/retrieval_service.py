from app.db.database import get_connection

#Distance and meaning
#  0.0–0.3 Very similar
#  0.3–0.5 Related
#  0.5–0.7 Weakly related
# 0.7–1.0 Barely related

def retrieve_similar_chunks(document_id,query_embedding, user_id, question, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    cursor.execute("""
        SELECT content,
               (1 / (1 + (embedding <-> %s))) AS semantic_score,
               ts_rank(content_tsv, plainto_tsquery('english', %s)) AS keyword_score,
               (
                 0.6 * (1 / (1 + (embedding <-> %s))) +
                 0.4 * ts_rank(content_tsv, plainto_tsquery('english', %s))
               ) AS final_score
        FROM aip.chunks
        WHERE user_id = %s AND document_id = %s
        ORDER BY final_score DESC
        LIMIT %s;
    """, (embedding_str,question,embedding_str,question, user_id, document_id, limit))

    results = cursor.fetchall()

    print(format(results))

    cursor.close()
    conn.close()

    # filter by threshold to get the most relevant result
    threshold = 0.9
    filtered = [row[0] for row in results if row[1] < threshold]

    return filtered