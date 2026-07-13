import json
import re


def parse_llm_json(text: str):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    return json.loads(text.strip())