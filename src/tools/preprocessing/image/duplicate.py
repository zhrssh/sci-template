import os
from hashlib import sha256

from tqdm import tqdm


def find_duplicate_images(directory):
    """Finds duplicate images in a directory.

    Args:
        directory (str): Directory to look for duplicate images

    Returns:
        list: List of duplicate images
    """
    # Dictionary to store hashes and corresponding filenames
    hash_dict = {}

    # List to store duplicate images
    duplicate_images = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            # Open the image file in binary mode and read its content
            with open(os.path.join(directory, filename), "rb") as img_file:
                img_data = img_file.read()

            # Calculate the MD5 hash of the image data
            img_hash = sha256(img_data).hexdigest()

            # Check if the hash already exists in the dictionary
            if img_hash in hash_dict:
                # If hash exists, it means the image is a duplicate
                duplicate_images.append((filename, hash_dict[img_hash]))
            else:
                # If hash doesn't exist, store it in the dictionary
                hash_dict[img_hash] = filename

    return duplicate_images


def delete_duplicate_images(duplicates, directory):
    """Delete duplicate images in the given directory.

    Args:
        duplicates (list): List of duplicate images from find_duplicate_images() function
        directory (str): path to the directory where the duplicate images are stored
    """
    for duplicate in tqdm(duplicates, desc="Deleting duplicates..."):
        duplicate_path = os.path.join(directory, duplicate[0])
        os.remove(duplicate_path)


if __name__ == "__main__":
    # Example usage
    directory = "."
    duplicates = find_duplicate_images(directory)
    delete_duplicate_images(duplicates, directory)
