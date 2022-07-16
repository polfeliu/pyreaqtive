import random
from pyreaqtive.models.sequence_matching import sequence_matching
from enum import Enum, auto
import pytest


class Operation(Enum):
    insert = auto()
    delete = auto()


@pytest.mark.parametrize("iteration", range(100))
def test_sequence_matcher(iteration):
    initial_list = random.sample(
        population=range(0, 100),
        k=random.randint(0, 50)
    )

    modified_list = initial_list.copy()

    for i_operation in range(random.randint(0, 30)):
        operation = random.choice(list(Operation))

        if operation == Operation.insert:
            index_on_the_list = random.randint(0, len(modified_list))

            for i in range(random.randint(0, 10)):
                modified_list.insert(
                    index_on_the_list,
                    random.randint(0, 10)
                )
        elif operation == Operation.delete:
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
