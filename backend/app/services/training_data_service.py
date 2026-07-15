import json


def save_sample(text, label):

    sample = {
        "text": text,
        "label": label
    }

    with open(
        "training_data.jsonl",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(sample) + "\n"
        )