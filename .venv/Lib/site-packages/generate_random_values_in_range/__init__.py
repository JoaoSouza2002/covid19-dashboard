import random
from math import ceil
from typing import Union


def get_true_false_percent(percent_true: int = 60) -> bool:
    return random.choices([True, False], [percent_true, 100 - percent_true])[0]


def randomize_number(
    value: Union[int, float],
    percent: int,
    percentage_substract_vs_add: int = 60,
    minimum_to_allow: Union[int, float, None] = None,
    maximum_to_allow: Union[int, float, None] = None,
) -> Union[float, int]:
    proba = get_true_false_percent(percent_true=int(percentage_substract_vs_add))
    try:
        if proba:
            randomno = value - (
                random.randrange(0, ceil(value / 100 * percent) * 1000) / 1000
            )
        else:
            randomno = value + (
                random.randrange(0, ceil(value / 100 * percent) * 1000) / 1000
            )

    except Exception:
        randomno = 0
    if minimum_to_allow is not None:
        if randomno < minimum_to_allow:
            randomno = minimum_to_allow
    if maximum_to_allow is not None:
        if randomno > maximum_to_allow:
            randomno = maximum_to_allow
    if isinstance(value, int):
        randomno = int(randomno)
    return randomno


if __name__ == "__main__":
    for _ in range(200):
        randval = randomize_number(
            value=620,
            percent=20,
            percentage_substract_vs_add=70,
            minimum_to_allow=580,
            maximum_to_allow=700,
        )
        if _ % 20 == 0:
            print("")
        print(randval, end=" ")

    print("\n\n")
    for _ in range(100):
        randval = get_true_false_percent(percent_true=80)
        if _ % 20 == 0:
            print("")
        if randval is True:
            print(randval, end="  ")
        else:
            print(randval, end=" ")
