from app.services.embedding_service import generate_embedding
from app.services.similarity_service import cosine_similarity


def find_similar_claims(
    text,
    examples
):

    query_embedding = generate_embedding(
        text
    )

    scores = []

    for example in examples:

        similarity = cosine_similarity(
            query_embedding,
            example["embedding"]
        )

        scores.append(
            (
                example,
                similarity
            )
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:5]