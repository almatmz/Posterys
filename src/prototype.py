"""Backward-compatible entry point for the component-based webcam prototype."""
import argparse

# Support both `python src/prototype.py` and `from src.prototype import ...`.
if __package__:
    from .posterys.app import main
    from .posterys.configuration import load_config
    from .posterys.detector import PostureDetector
    from .posterys.measurements import angle_difference, measure
else:
    from posterys.app import main
    from posterys.configuration import load_config
    from posterys.detector import PostureDetector
    from posterys.measurements import angle_difference, measure


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Posterys local webcam prototype")
    parser.add_argument("--config", help="Path to an optional JSON configuration file")
    args = parser.parse_args()
    try:
        config = load_config(args.config)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    main(config)
