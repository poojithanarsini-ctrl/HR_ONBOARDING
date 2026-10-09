
from sentence_transformers import SentenceTransformer

# Load a lightweight model for creating text embeddings.
# The first run may download the model.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    """Load the embedding model only when needed."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def create_embeddings(texts):
    """Convert a list of text strings into numerical vectors."""
    if isinstance(texts, str):
        texts = [texts]

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings


def create_query_embedding(query):
    """Create an embedding for one employee question."""
    return create_embeddings([query])[0]