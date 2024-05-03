from pathlib import Path

import cv2
import numpy as np
import pillow_heif
from PIL import Image, ImageFile, ExifTags
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


def compress_images(directory: Path, *, reduce_to: float = 0.60):
    """
    This function compresses all images in a given directory to a maximum width, maintaining aspect ratio.
    It uses the Pillow library to read, resize, and save the images.

    Args:
        directory (Path): The directory containing the images to be compressed.
        reduce_to (float, optional): Reduce the size of the image to the given percentage. Defaults to 0.60.

    Returns:
        None. The function saves the compressed images in the original directory.
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for fpath in tqdm(list(directory.iterdir()), desc="Compressing images..."):
        if fpath.is_dir():
            compress_images(fpath, reduce_to=reduce_to)
            continue

        if fpath.suffix != ".heic":  # Heic is not supported in Pillow
            # Read image file
            image = Image.open(fpath.__str__())

            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif:
                    for tag, label in ExifTags.TAGS.items():
                        if label == 'Orientation':
                            orientation = tag
                            break
                    if orientation in exif:
                        if exif[orientation] == 3:
                            image = image.rotate(180, expand=True)
                        elif exif[orientation] == 6:
                            image = image.rotate(270, expand=True)
                        elif exif[orientation] == 8:
                            image = image.rotate(90, expand=True)

            # Resize the original image
            image = image.resize(
                (round(image.size[0] * reduce_to), round(image.size[1] * reduce_to))
            )

            # Save the compressed image
            image.save(
                Path(*fpath.parts[:-1], f"{fpath.stem}.jpg").__str__(),
                optimize=True,
                quality=90,
            )


if __name__ == "__main__":
    # Example usage
    filepaths = list(Path(".").glob("*.heic"))
    for file in tqdm(filepaths, desc="Converting files", total=len(filepaths)):
        output_folder_path = Path("output")
        heic_to_png(file, output_folder_path)

    print("Done!")
