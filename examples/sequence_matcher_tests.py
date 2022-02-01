import difflib

a = [1, 2, 3, 5, 6, 7, 8, 9]
b = [2, 3, 6, 7, 8, 10, 11]

print(a)
print(b)

# Objective: Modify a so it is the same as b

seq_mat = difflib.SequenceMatcher(a=a, b=b)

operations = seq_mat.get_opcodes()

running_shift = 0


def delete(i1: int, i2: int):
    global running_shift
    del a[i1 + running_shift:i2 + running_shift]


def insert(i: int, l: list):
    global running_shift
    for k, item in enumerate(l):
        a.insert(i + running_shift + k, item)


for code, i1, i2, j1, j2 in operations:
    print(code)

    if code == 'equal':
        pass
    elif code == 'delete':
        delete(i1, i2)
        running_shift += i1 - i2
    elif code == 'replace':
        delete(i1, i2)
        insert(i1, b[j1: j2])
        running_shift += (j2 - j1) - (i1 - i2)

    # TODO Insert
    else:
        raise NotImplementedError(code)

print(running_shift)
print(a)
