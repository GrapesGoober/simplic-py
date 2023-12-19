start:
    set 0   0   # 'previous' at 0
    set 1   1   # 'current' at 1
    set 2   2   # 'next' at 2
    set 3   2   # 'counter' at 3
    set 4   1   # 'increment' at 4
    set 5   24  # 'max' at 5

loop:
    load    0   # next = previous + current    
    add     1
    store   2
    load    1   # previous = current
    store   0
    load    2   # current = next
    store   1

    # compare counter and max, how?

    load    3   # counter += increment
    add     4 
    store   3
    jump    loop

start:
    jump loop


    