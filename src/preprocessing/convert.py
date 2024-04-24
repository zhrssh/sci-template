from pathlib import Path

import cv2
import numpy as np
import pillow_heif
from tqdm import tqdm


def heic_to_png(
    source: Path,
    destination: Path,
    convert_hdr_to_8bit: bool = False,
    bgr_mode: bool = True,
    **heic_options,
) -> None:
    """Converts a directory of HEIC files to PNG format.

    Args:
        source (Path): The directory containing the HEIC files.
        destination (Path): The directory where the PNG files will be saved.
        convert_hdr_to_8bit (bool, optional): Whether to convert high dynamic range images to 8-bit. Defaults to False.
        bgr_mode (bool, optional): Whether to open the image in BGR mode. Defaults to True.
        **heic_options: Additional options to pass to the pillow-heif library.

    Raises:
        ValueError: If the source or destination directories do not exist.

    Returns:
        None
    """
    if not destination.exists():
        destination.mkdir()

    # Get the list of heic files to convert to png
    fpaths = []
    for path in list(source.iterdir()):
        if path.is_dir():
            heic_to_png(
                path,
                destination,
                convert_hdr_to_8bit=convert_hdr_to_8bit,
                bgr_mode=bgr_mode,
                **heic_options,
            )
            continue

        if path.suffix.lower() == ".heic":
            fpaths.append(path)

    # Convert all heic files to png files
    for fpath in tqdm(fpaths, desc="Converting HEIC to PNG..."):
        fname = fpath.name.split(".")[0] + ".png"
        heif_file = pillow_heif.open_heif(
            fpath.__str__(),
            convert_hdr_to_8bit=convert_hdr_to_8bit,
            bgr_mode=bgr_mode,
            **heic_options,
        )
        np_array = np.asarray(heif_file)
        cv2.imwrite(Path(destination, fname).__str__(), np_array)

        # Removes the old image
        fpath.unlink(missing_ok=True)


def convert_images(
    source: Path, destination: Path = None, to_format: str = "png"
) -> None:
    """Converts a directory of images to a specified format.

    Args:
        source (Path): The directory containing the images.
        destination (Path, optional): The directory where the converted images will be saved. If not specified, the images will be saved in the same directory as the original images.
        to_format (str, optional): The format to convert the images to. Defaults to "png".

    Raises:
        ValueError: If the source directory does not exist or if the to_format is not supported.

    Returns:
        None
    """
    for path in tqdm(
        list(source.iterdir()), desc=f"Converting images to {to_format} format..."
    ):
        if path.is_dir():
            convert_images(path, destination, to_format=to_format)
            continue

        # Check if the path is not the corrected format
        ext = f".{to_format}"
        if path.suffix != ext:
            img = cv2.imread(path.__str__())

            # Saves the image
            if destination is not None:
                new_path = Path(destination, path.name.split(".")[0] + ext)
                cv2.imwrite(new_path.__str__(), img)
            else:
                cv2.imwrite(path.__str__().split(".")[0] + ext, img)

            # Removes the old image
            path.unlink(missing_ok=True)
