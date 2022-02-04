import difflib


def sequence_matching(modifiable_list: list, target_list: list):
    """
    Modifies a list so it's the same as an other one, applying insert and delete operations

    Args:
        modifiable_list: list that has to be modified
        target_list: list that must be copied
    """
    seq_mat = difflib.SequenceMatcher(a=modifiable_list, b=target_list)

    operations = seq_mat.get_opcodes()

    running_shift = 0

    for code, i1, i2, j1, j2 in operations:

        if code == 'equal':
            # modifiable_list[i1:i2] == target_list[j1:j2] (the sub-sequences are equal).
            pass
        elif code == 'delete':
            # modifiable_list[i1:i2] should be deleted. Note that j1 == j2 in this case.
            del modifiable_list[i1 + running_shift:i2 + running_shift]
            running_shift += i1 - i2

            print(f"### delete [{i1 + running_shift}:{i2 + running_shift}]")

        elif code == 'replace':
            # modifiable_list[i1:i2] should be replaced by target_list[j1:j2].
            print("### Replace")

            # Delete
            del modifiable_list[i1 + running_shift:i2 + running_shift]

            print(f"#delete [{i1 + running_shift}:{i2 + running_shift}]")

            # Insert
            for k, item in enumerate(target_list[j1:j2]):
                modifiable_list.insert(i1 + running_shift + k, item)

            print(f"# insert sequence {target_list[j1:j2]} to {i1 + running_shift}")

            running_shift += (j2 - j1) - (i2 - i1)

        elif code == 'insert':
            # target_list[j1:j2] should be inserted at modifiable_list[i1:i1]. Note that i1 == i2 in this case.

            print(f"### insert sequence {target_list[j1:j2]} to {i1 + running_shift}")
            for k, item in enumerate(target_list[j1:j2]):
                modifiable_list.insert(i1 + running_shift + k, item)
            running_shift += (j2 - j1)
        else:
            raise NotImplementedError(code)

        print(f"Modifiable list {modifiable_list}")
        print(f"Running shift {running_shift}")
