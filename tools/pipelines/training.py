from array import ArrayType
from typing import Any, Callable


def train_model(
    model_builder: Callable,
    model_args: dict[str, Any],
    X: ArrayType,
    y: ArrayType,
    **training_args
):
    raise NotImplementedError()


def train_model_ml(
    model_builder: Callable,
    model_args: dict[str, Any],
    X: ArrayType,
    y: ArrayType,
    **training_args
):
    raise NotImplementedError()
