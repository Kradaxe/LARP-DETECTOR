def update_weights(
    old_weight,
    correction
):
    learning_rate = 0.05

    return old_weight + (
        learning_rate * correction
    )