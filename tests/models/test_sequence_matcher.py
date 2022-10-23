from enum import Enum, auto
import random

import pytest

from pyreaqtive.models.sequence_matching import sequence_matching


class Operation(Enum):
    INSERT = auto()
    DELETE = auto()


@pytest.mark.parametrize("iteration", range(100))
def test_sequence_matcher(
        iteration: int  # pylint: disable=unused-argument
) -> None:
    initial_list = random.sample(
        population=range(0, 100),
        k=random.randint(0, 50)
    )

    modified_list = initial_list.copy()

    for _ in range(random.randint(0, 30)):
        operation = random.choice(list(Operation))

        if operation == Operation.INSERT:
            index_on_the_list = random.randint(0, len(modified_list))

            for _ in range(random.randint(0, 10)):
                modified_list.insert(
                    index_on_the_list,
                    random.randint(0, 10)
                )
        elif operation == Operation.DELETE:
            start = random.randint(0, len(modified_list))
            end = random.randint(start, len(modified_list))
            del modified_list[start:end]
        else:
            raise NotImplementedError

    # Sometimes completely replace the list
    if random.randint(0, 100) < 5:
        # 5 Percent of lists, replace the list entirely
        modified_list = random.sample(
            population=range(0, 100),
            k=random.randint(0, 10)
        )

    sequence_matching(initial_list, modified_list)

    if modified_list != initial_list:
        raise AssertionError
