import nltk

def chunk_text(text, chunk_size=300, overlap=1):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_length + sentence_length > chunk_size:
            chunks.append(" ".join(current_chunk))

            # overlap last N sentences with overlapo limit
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks