from sentence_transformers import SentenceTransformer, CrossEncoder

#Bi encoder
_embedding_model = None

#Crossencoder
_cross_encoder = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-mpnet-base-v2")
    return _embedding_model


def get_cross_encoder():
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _cross_encoder