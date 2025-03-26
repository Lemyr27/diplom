from sentence_transformers import SentenceTransformer


def get_embedding(text: str) -> list[float]:
    model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2', truncate_dim=512)
    return model.encode(text).tolist()
