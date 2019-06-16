from typing import Union


def mod(x: Union[float, int]) -> Union[float, int]:
    if x < 0:
        return -x
    return x
