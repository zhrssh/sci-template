from pathlib import Path

# Directories
PROJECT_DIR = Path(*Path(__file__).parts[:-4])
REPORTS_DIR = Path(PROJECT_DIR, "reports")
MODELS_DIR = Path(PROJECT_DIR, "models")

# Dataset Directories
RAW_DATASET_DIR = Path(PROJECT_DIR, r"data\raw")
PROCESSED_DATASET_DIR = Path(PROJECT_DIR, r"data\processed")
EXTERNAL_DATASET_DIR = Path(PROJECT_DIR, r"data\external")
