from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer(
    'sentence-transformers/distiluse-base-multilingual-cased-v2',
    truncate_dim=512,
)


def get_embedding(text: str) -> list[float]:
    return MODEL.encode(text).tolist()
