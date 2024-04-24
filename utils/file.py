from pathlib import Path

from tqdm import tqdm


def rename_files(source: Path, name: str):
    """Renames files in the given directory.

    Args:
        directory (Path): The directory containing the files to rename.
        name (str): The base name to use for the renamed files.

    Raises:
        ValueError: If the given directory does not exist or is not a directory.

    Returns:
        None
    """
    for idx, file in tqdm(enumerate(list(source.iterdir())), desc="Renaming files"):
        if file.is_dir():
            continue

        new_name = f"{name}_{idx + 1}{file.suffix}"
        new_path = Path(source, new_name)

        # Skip renamed files
        if new_path.exists():
            continue

        file.rename(new_path)
