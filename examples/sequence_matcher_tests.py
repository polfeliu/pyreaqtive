import difflib

a = [1, 2, 3, 4, 5, 6, 7, 8]
b = [1, 5, 2, 3, 4, 5, 7, 8, 9]
# b = [2, 3, 6, 4, 7, 8, 10, 11]

print(f"Original a {a}")
print(f"Original b {b}")

# Objective: Modify a so it is the same as b

seq_mat = difflib.SequenceMatcher(a=a, b=b)

operations = seq_mat.get_opcodes()

running_shift = 0


def delete(i1: int, i2: int):
    global running_shift
    global a
    del a[i1 + running_shift:i2 + running_shift]


def insert(i: int, l: list):
    global running_shift
    global a
    for k, item in enumerate(l):
        a.insert(i + running_shift + k, item)


for code, i1, i2, j1, j2 in operations:

    if code == 'equal':
        # a[i1:i2] == b[j1:j2] (the sub-sequences are equal).
        pass
    elif code == 'delete':
        # a[i1:i2] should be deleted. Note that j1 == j2 in this case.
        delete(i1, i2)
        running_shift += i1 - i2
    elif code == 'replace':
        # a[i1:i2] should be replaced by b[j1:j2].
        delete(i1, i2)
        insert(i1, b[j1:j2])
        running_shift += (j2 - j1) - (i1 - i2)
    elif code == 'insert':
        # b[j1:j2] should be inserted at a[i1:i1]. Note that i1 == i2 in this case.
        insert(i1, b[j1:j2])
        running_shift += (j2 - j2) + 1
    else:
        raise NotImplementedError(code)

    print(f"### {code}")
    print(a)
    print(running_shift)

print(f"Original b {b}")
print(f"Modified a {a}")

if len(a) != len(b):
    raise AssertionError

for i in range(len(a)):
    if a[i] != b[i]:
        raise AssertionError
