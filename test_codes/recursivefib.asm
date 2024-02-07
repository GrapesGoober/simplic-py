func_main:
    set      2,      24
    stack    push
    set      0,      func_main.return_0
    stack    pop
    load     2
    stack    push
    store    1
    if       always,         fib_recursive
func_main.return_0:
    load     1
    stack    pop
    store    1
    set      0,      %halt
    load     0
    set      0,      0
    storem   0
add_til_ten:
    set      3,      10
    load     1
    sub      3
    if       less,   add_til_ten.recurse
    load     1
    store    1
    load     0
    set      0,      0
    storem   0
add_til_ten.recurse:
    set      4,      1
    load     1
    add      4
    store    2
    stack    push
    set      0,      add_til_ten.return_0
    stack    pop
    load     2
    stack    push
    store    1
    if       always,         add_til_ten
add_til_ten.return_0:
    load     1
    stack    pop
    store    1
    load     0
    set      0,      0
    storem   0
fib_iterative:
    start:
    set      1,      1
    set      2,      1
    set      3,      0
    set      4,      2
    set      5,      1
    set      6,      24
loop:
    load     1
    add      2
    store    3
    load     2
    store    1
    load     3
    store    2
    load     4
    add      5
    store    4
    load     4
    sub      6
    if       less,   loop
    load     2
    store    1
    load     0
    set      0,      0
    storem   0
fib_recursive:
    set      3,      1
    load     1
    sub      3
    if       more,   fib_recursive.recurse
    load     1
    store    1
    load     0
    set      0,      0
    storem   0
fib_recursive.recurse:
    set      3,      1
    load     1
    sub      3
    store    4
    stack    push
    set      0,      fib_recursive.return_0
    stack    pop
    load     4
    stack    push
    store    1
    if       always,         fib_recursive
fib_recursive.return_0:
    load     1
    stack    pop
    store    5
    set      3,      2
    load     1
    sub      3
    store    4
    stack    push
    set      0,      fib_recursive.return_1
    stack    pop
    load     4
    stack    push
    store    1
    if       always,         fib_recursive
fib_recursive.return_1:
    load     1
    stack    pop
    store    6
    load     5
    add      6
    store    2
    load     2
    store    1
    load     0
    set      0,      0
    storem   0