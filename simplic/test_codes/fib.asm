variables:
    current     0
    previous    1
    counter     2

start:
    insert  1
    store   current

loop:
    load    current
    add     previous
    