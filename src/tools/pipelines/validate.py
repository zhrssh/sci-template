from array import ArrayType
from typing import Any, Callable


def validate_by_kfold(
    model_builder: Callable,
    model_args: dict[str, Any],
    X: ArrayType,
    y: ArrayType,
    *,
    n_splits: int = 10,
    use_stratified: bool = True,
    **kwargs
):
    raise NotImplementedError()
