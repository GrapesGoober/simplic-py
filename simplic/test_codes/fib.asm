start:
    insert  0   # 'previous' at 0
    store   0   
    insert  1   # 'current' at 1
    store   1   
    insert  0   # 'next' at 2
    store   2   
    insert  2   # 'counter' at 3
    store   3   
    insert  1   # 'increment' at 4
    store   4   
    insert  1   # 'max' at 5
    insert  8   #     count up to 24th fib
    store   5   #     which is 0x18

loop:  s
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


    