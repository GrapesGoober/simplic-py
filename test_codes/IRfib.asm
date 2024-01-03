label   fibbonaci.start
set     0       1     
set     1       1     
set     2       0     
set     3       2     
set     4       1     
set     5       24    
label   fibbonaci.loop
load    0
add     1
store   2
load    1
store   0
load    2
store   1
load    3
add     4
store   3
load    3
sub     5
if      less    fibbonaci.loop