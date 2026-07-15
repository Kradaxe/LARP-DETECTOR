import numpy as np


def cosine_similarity(
    vector_a,
    vector_b
):

    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(
        a,
        b
    ) / (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )