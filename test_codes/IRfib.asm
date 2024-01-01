label   fibbonaci.start
set     1       1     
set     2       1     
set     3       0     
set     4       2     
label   fibbonaci.loop
load    1
add     2
store   3
load    2
store   1
load    3
store   2
load    4
set     5       1
add     5
store   4
load    4
set     5       24
sub     5
if      less    fibbonaci.loop