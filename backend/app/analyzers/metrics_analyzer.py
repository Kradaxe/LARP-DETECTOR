# app/analyzers/metrics_analyzer.py

import re
from typing import Dict, List


METRIC_PATTERN = r'\b\d+(\.\d+)?(%|ms|s|gb|mb|tb|x)?\b'


def analyze_metrics(text: str) -> Dict:
    matches = re.findall(METRIC_PATTERN, text)

    return {
        "metrics_count": len(matches)
    }