from typing import Optional, Union


def to_float(val: Optional[Union[float, int]]) -> float:
    if isinstance(val, float):
        return val
    elif isinstance(val, int):
        return float(val)
    return


def to_percent_used(total: Optional[int], free: Optional[int]) -> float:
    if free is None or total is None or total <= 0:
        return
    return (1 - free / total) * 100
