import app.db.database as db
from app.helpers.terminalColor import red,green,yellow

def insert_documents_metadata(document_id, user_id, conn, cursor, file_name, file_path):
    try:
        cursor.execute("""
                      INSERT INTO aip.documents(id, user_id, file_name, file_path) VALUES (%s, %s, %s, %s)
                      """, (document_id, user_id, file_name, file_path))
    except Exception as e:
        print(f"{red}[ERROR]: While inserting document metadata: {e} \n Rolling back")
        conn.rollback()

