label   fibbonaci.start
set     1       1
set     2       1
set     3       0
set     4       2
set     5       1
set     6       24
label   fibbonaci.loop
load    1
add     2
store   3
load    2
store   1
load    3
store   2
load    4
add     5
store   4
load    4
stack   push
store   2
load    3
add     2
store   3
stack   pop
load    4
sub     6
if      less    fibbonaci.loop
stack   push
load    2
stack   pop
store   13
stack   push
load    3
stack   pop
store   14