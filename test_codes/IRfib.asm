label   fibbonaci.start
set     3       1
set     4       1
set     5       0
set     6       2
label   fibbonaci.loop
load    3
add     4
store   5
load    4
store   3
load    5
store   4
load    6
set     7       1
add     7
store   6
load    6
set     7       24
sub     7
if      less    fibbonaci.loop