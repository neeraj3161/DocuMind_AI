import uuid

class Chunk:
    page_number = 0
    def __init__(self, document_id, user_id, chunk_index, content, embedding):
        self.document_id = document_id
        self.user_id = user_id
        self.chunk_index = chunk_index
        self.content = content
        self.embedding = embedding
        self.page_number = self.page_number
