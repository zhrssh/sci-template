from pathlib import Path

import cv2
import numpy as np
import pillow_heif
from PIL import Image, ImageFile
from tqdm import tqdm


def heic_to_png(heic_file: Path, output_folder: Path):
    """Convert a heic file to a png file.

    Args:
        heic_file (Path): Filepath of the heic file.
        output_folder (Path): Destination folder.
    """
    if not output_folder.exists():
        output_folder.mkdir()

    fname = heic_file.name.split(".")[0] + ".png"
    heif_file = pillow_heif.open_heif(
        heic_file.__str__(), convert_hdr_to_8bit=False, bgr_mode=True
    )
    np_array = np.asarray(heif_file)
    cv2.imwrite(Path(output_folder, fname).__str__(), np_array)

    # Removes the old image
    heic_file.unlink(missing_ok=True)


def images_to_png(directory: Path, destination: Path = None):
    """Converts images in the given directory to png.

    Args:
        directory (Path): Directory to convert images to png.
        destination (Path, optional): Destination folder. Defaults to None.
    """
    for path in tqdm(list(directory.iterdir()), desc="Converting images..."):
        if path.is_dir():
            images_to_png(path, destination)
            continue

        if path.suffix != ".png":
            img = cv2.imread(path.__str__())

            # Saves the image
            if destination is not None:
                new_path = Path(destination, path.name.split(".")[0] + ".png")
                cv2.imwrite(new_path.__str__(), img)
            else:
                cv2.imwrite(path.__str__().split(".")[0] + ".png", img)

            # Removes the old image
            path.unlink(missing_ok=True)


def compress_image(directory: Path, *, max_size: int):
    """
    This function compresses all images in a given directory to a maximum width, maintaining aspect ratio.
    It uses the Pillow library to read, resize, and save the images.

    Args:
        directory (Path): The directory containing the images to be compressed.
        max_width (int): The maximum width of the compressed images.

    Returns:
        None. The function saves the compressed images in the original directory.
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for fpath in tqdm(list(directory.iterdir()), desc="Compressing images..."):
        if fpath.is_dir():
            compress_image(fpath, max_size=max_size)
            continue

        if fpath.suffix != ".heic":  # Heic is not supported in Pillow
            # Read image file
            image = Image.open(fpath.__str__())

            # Get image size and aspect ratio
            width, height = image.size
            aspect_ratio = width / height

            # Resize the image while preserving aspect ratio
            if width > height:
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(max_size * aspect_ratio)

            # Resize the original image
            image = image.resize((new_width, new_height))

            # Save the compressed image
            image.save(fpath.__str__(), optimize=True, quality=90)


if __name__ == "__main__":
    # Example usage
    filepaths = list(Path(".").glob("*.heic"))
    for file in tqdm(filepaths, desc="Converting files", total=len(filepaths)):
        output_folder_path = Path("output")
        heic_to_png(file, output_folder_path)

    print("Done!")
