variables = [
    ("a", 1, 2),
    ("b", 1, 3),
    ("c", 1, 1),
    ("d", 2, 5),
    ("e", 3, 5),
]

for n, _, _ in variables:
    print(n, end="  ")
print()

# BEGIN
registers = [f"r{i}" for i in range(1,10)]
alloc = {}

for t in range(1, 10):
    for v, start, end in variables:
        if t in range(start, end+1):
            # in range, not allocated
            if v not in alloc:
                # start allocating
                alloc[v] = registers[0]
                registers.pop(0)
            # in range, allocated
            print(alloc[v], end=" ")
        else:
            # out of range, unallocated
            if v in alloc:
                registers.insert(0, alloc[v])
                alloc.pop(v)
            print("   ", end="")
            
    print()