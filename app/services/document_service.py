import uuid
import app.db.database as db

def insert_documents_metadata(document_id, user_id, file_name, file_path):
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
              INSERT INTO aip.documents(id, user_id, file_name, file_path) VALUES (%s, %s, %s, %s)
              """, (document_id, user_id, file_name, file_path))
    connection.commit()
    cursor.close()
    connection.close()
