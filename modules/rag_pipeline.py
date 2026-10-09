from modules.embeddings import create_embeddings, create_query_embedding


def split_text(text, chunk_size=500, overlap=50):
    """Split policy text into smaller overlapping chunks."""
    text = text.strip()

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def index_policy_text(text):
    """Prepare policy text and create embeddings."""
    chunks = split_text(text)

    if not chunks:
        return {"chunks": [], "embeddings": None}

    embeddings = create_embeddings(chunks)

    return {
        "chunks": chunks,
        "embeddings": embeddings,
    }


def search_policy(question, indexed_policy, top_k=3):
    """Find the policy chunks most relevant to a question."""
    chunks = indexed_policy["chunks"]
    embeddings = indexed_policy["embeddings"]

    if not chunks or embeddings is None:
        return []

    query_embedding = create_query_embedding(question)

    # Embeddings are normalized, so dot product gives cosine similarity.
    similarities = embeddings @ query_embedding

    top_indices = similarities.argsort()[::-1][:top_k]

    return [
        {
            "text": chunks[int(i)],
            "score": float(similarities[i]),
        }
        for i in top_indices
    ]
