# Prototype configuration

The current application is the local Python webcam prototype. No server, database,
API credentials or environment variables are required.

Run from the repository root using the existing default command:

```sh
python src/prototype.py
```

Or use the supplied configuration example:

```sh
python src/prototype.py --config config/prototype.example.json
```

Copy the example to another JSON file to customise it and pass that path to
`--config`. Paths are relative to the current working directory.

| Key | Default | Meaning |
| --- | --- | --- |
| `camera_index` | `0` | Non-negative OpenCV camera device index. |
| `min_detection_confidence` | `0.5` | MediaPipe pose detection confidence, from 0 to 1. |
| `min_tracking_confidence` | `0.5` | MediaPipe pose tracking confidence, from 0 to 1. |

Omitted keys use the defaults. Unknown keys and invalid values are rejected before
camera startup. These options do not change the experimental assessment thresholds
or establish clinical accuracy. Camera frames remain local and are not recorded.

Install runtime dependencies with `python -m pip install -r requirements.txt` in
the Python 3.10 environment described in the main README. The correctly named
`requirements.txt` contains the existing pinned versions. The legacy
`requiremetns.txt` is retained unchanged for compatibility.
