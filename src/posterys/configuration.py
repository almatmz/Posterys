"""Optional JSON configuration; no external configuration dependency."""
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "camera_index": 0,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
}


def load_config(path=None):
    config = DEFAULT_CONFIG.copy()
    if path is None:
        return config
    values = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(values, dict):
        raise ValueError("Configuration must be a JSON object")
    unknown = values.keys() - config.keys()
    if unknown:
        raise ValueError("Unknown configuration keys: " + ", ".join(sorted(unknown)))
    config.update(values)
    index = config["camera_index"]
    if type(index) is not int or index < 0:
        raise ValueError("camera_index must be a non-negative integer")
    for key in ("min_detection_confidence", "min_tracking_confidence"):
        value = config[key]
        if type(value) not in (int, float) or not 0 <= value <= 1:
            raise ValueError(key + " must be a number between 0 and 1")
    return config
