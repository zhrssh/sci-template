from hashlib import sha256
from pathlib import Path

from tqdm import tqdm


def find_duplicate_images(directory: Path) -> list[tuple[Path, Path]]:
    """
    This function takes a directory path as input and scans it for duplicate images.
    It calculates the SHA256 hash of each image and stores it in a dictionary, along with the corresponding file path.
    If the same hash is encountered again, it means that the image is a duplicate and is added to a list of duplicates.

    Args:
        directory (Path): The directory path to scan for duplicate images

    Returns:
        list[tuple[Path, Path]]: A list of tuples, where each tuple represents a duplicate image, consisting of the duplicate file path and the original file path
    """
    # Dictionary to store hashes and corresponding filenames
    hash_dict = {}

    # List to store duplicate images
    duplicate_images = []

    # Iterate through all files in the directory
    for path in directory.iterdir():
        if path.suffix in (".jpg", ".jpeg", ".png"):
            with open(path.__str__(), "rb") as img_file:
                img_data = img_file.read()

            # Calculate the SHA256 hash of the image data
            img_hash = sha256(img_data).hexdigest()

            # Check if the hash already exists in the dictionary
            if img_hash in hash_dict:
                # If hash exists, it means the image is a duplicate
                duplicate_images.append((path, hash_dict[img_hash]))
            else:
                # If hash doesn't exist, store it in the dictionary
                hash_dict[img_hash] = path

    return duplicate_images


def delete_duplicate_images(
    duplicates: list[tuple[Path, Path]], missing_ok: bool = True
):
    """
    This function takes a list of tuples, where each tuple represents a duplicate image, and deletes the duplicate files.
    It also provides an option to skip deleting files that do not exist.

    Args:
        duplicates (list[tuple[Path, Path]]): A list of tuples, where each tuple represents a duplicate image, consisting of the duplicate file path and the original file path
        missing_ok (bool, optional): A boolean value indicating whether to skip deleting files that do not exist. Defaults to True.

    Raises:
        ValueError: If the input list contains tuples that do not contain file paths
    """
    for duplicate_tuple in tqdm(duplicates, desc="Deleting duplicates..."):
        if duplicate_tuple[0].is_dir():
            raise ValueError("Duplicate must be a file. Not a directory.")

        duplicate_tuple[0].unlink(missing_ok)
