label   func.start
set     0       1
set     1       1
set     2       0
set     3       2
label   func.loop
load    0        
add     1        
store   2        
load    1        
store   0        
load    2        
store   1        
load    3        
set     4       1
add     4        
store   3        
load    3
set     4       24
sub     4
if      less    func.loop