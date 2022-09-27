from typing import TYPE_CHECKING, Union

import difflib

if TYPE_CHECKING:
    from .rqlist import RQList


def sequence_matching(modifiable_list: Union[list, 'RQList'], target_list: list) -> None:
    """List Sequence Matching.

    Modifies a list so it's the same as an other one, applying insert and delete operations

    Args:
        modifiable_list: list that has to be modified
        target_list: list that must be copied
    """
    seq_mat = difflib.SequenceMatcher(a=modifiable_list, b=target_list)

    operations = seq_mat.get_opcodes()

    running_shift = 0

    for code, i1, i2, j1, j2 in operations:  # pylint: disable=invalid-name

        if code == 'equal':
            # modifiable_list[i1:i2] == target_list[j1:j2] (the sub-sequences are equal).
            pass
        elif code == 'delete':
            # modifiable_list[i1:i2] should be deleted. Note that j1 == j2 in this case.

            del modifiable_list[i1 + running_shift:i2 + running_shift]
            running_shift += i1 - i2

        elif code == 'replace':
            # modifiable_list[i1:i2] should be replaced by target_list[j1:j2].

            # Delete
            del modifiable_list[i1 + running_shift:i2 + running_shift]

            # Insert
            for k, item in enumerate(target_list[j1:j2]):
                modifiable_list.insert(i1 + running_shift + k, item)

            running_shift += (j2 - j1) - (i2 - i1)

        elif code == 'insert':
            # target_list[j1:j2] should be inserted at modifiable_list[i1:i1]. Note that i1 == i2 in this case.

            for k, item in enumerate(target_list[j1:j2]):
                modifiable_list.insert(i1 + running_shift + k, item)

            running_shift += (j2 - j1)
        else:
            raise NotImplementedError(code)  # pragma: no cover
