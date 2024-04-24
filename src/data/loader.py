import shutil
from pathlib import Path

import tensorflow as tf
from keras.layers import Rescaling
from keras.utils import image_dataset_from_directory
from tqdm import tqdm


def arrange_for_classification(
    source: Path,
    destination: Path,
    sep: str = "_",
    class_index: int = 0,
    copy: bool = True,
) -> None:
    """This function is used to arrange the files in a directory based on their class labels.

    Args:
        source (Path): The path of the source directory.
        destination (Path): The path of the destination directory. If None, the files will be copied to a directory with the same name as the source directory, but with the class labels as subdirectories.
        sep (str, optional): The separator used to split the class labels from the file names. Defaults to "_".
        class_index (int, optional): The index of the class label in the file name. Defaults to 0.
        copy (bool, optional): Whether to copy the files or move them. Defaults to True.
    """
    # Make directory for destination directory
    if destination is not None:
        destination.mkdir(exist_ok=True)

    # Get all the list of all files
    fpaths = []
    for path in list(Path(source).iterdir()):
        # Check if path is a directory
        if path.is_dir():
            arrange_for_classification(
                path, destination, sep=sep, class_index=class_index, copy=copy
            )
            continue

        fpaths.append(Path(path))

    # Move all file paths to new directory
    for path in tqdm(fpaths, desc="Arranging files for classification..."):
        # Get the class label
        target = path.stem.split(sep)[class_index]

        # Prepare path for target file
        target_dir = (
            Path(source, target) if destination is None else Path(destination, target)
        )

        # Make directory for target file if not exists
        target_dir.parent.mkdir(parents=True, exist_ok=True)

        # Moves or copy the dataset to the target path
        if copy:
            shutil.copy(path, target_dir)
        else:
            shutil.move(path, target_dir)

    print("Done!")


def load_image_dataset(
    src_dir: str,
    class_names: list[str],
    image_size: tuple[int, int],
    batch_size: int = None,
    validation_split: float = 0.2,
    normalized: bool = True,
    **kwargs,
) -> tuple[tf.data.Dataset, tf.data.Dataset]:
    """Loads image dataset from a directory.

    Args:
        src_dir (str): The directory path.
        class_names (list[str]): The list of class names.
        image_size (tuple[int, int]): The size of the images.
        batch_size (int, optional): The batch size. Defaults to None.
        validation_split (float, optional): The validation split. Defaults to 0.2.
        normalized (bool, optional): Whether to normalize the data. Defaults to True.
        **kwargs: Additional arguments for the `image_dataset_from_directory` function.

    Returns:
        tuple[tf.data.Dataset, tf.data.Dataset]: A tuple containing the training and validation datasets.
    """

    train_ds, val_ds = image_dataset_from_directory(
        src_dir,
        class_names=class_names,
        image_size=image_size,
        batch_size=batch_size,
        validation_split=validation_split,
        subset="both",
        **kwargs,
    )

    # Configures the dataset for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Standardizes the data
    if normalized:
        normalization_layer = Rescaling(1.0 / 255)
        train_ds_norm = train_ds.map(lambda x, y: (normalization_layer(x), y))
        val_ds_norm = val_ds.map(lambda x, y: (normalization_layer(x), y))

        return (train_ds_norm, val_ds_norm)
    else:
        return (train_ds, val_ds)
