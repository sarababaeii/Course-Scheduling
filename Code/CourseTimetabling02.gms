* Course Timetabling Problem

set
    c 
    l 
    d 
    h 
    j;
    
singleton set
    last_d(d);

alias(d, d1);
alias(h, h1);

parameter
    k      
    n(c)        
    u(c)        
    s(j, c)
    a(c, l)
    b(l, d, h)
    f(h)        
    g(h)        
    t(h, h1)    
    M           
    opt_z1
    opt_z2;

$gdxIn %gdxincname%
$load c, l, d, last_d, h, j, k, n, u, s, a, b, f, g, t, M
$gdxIn

variable z1, z2, z3;
nonnegative variable w, v(c, d);
binary variable delta(c, d, h), gamma(c);

equation obj0, obj1, obj2, obj3,
         const1, const2, const3, const4, const5, const6,
         const7, const8, const9,
         const10, const11;

* Objective Functions:

obj1..
    z1 =e= w;
    
obj2..
    z2 =e= sum(c $ (n(c) > 1), sum(d $ (d.val < last_d.val), v(c, d)));
    
obj3..
    z3 =e= sum(c $ (n(c) > 1), gamma(c));
    
* Hard Constraints:

const1(c)..
    sum((d, h) $ (g(h) = u(c)), delta(c, d, h)) =e= n(c);
    
const2(d, h, h1) $ (g(h) = 1 and g(h1) = 0 and t(h, h1) = 1)..
    sum(c $ (u(c) = 1), delta(c, d, h)) + sum(c $ (u(c) = 0), delta(c, d, h1)) =l= k;

    
const3(l, d, h, h1) $ (g(h) = 1 and g(h1) = 0 and t(h, h1) = 1)..
    sum(c $ (u(c) = 1 and a(c, l) = 1), delta(c, d, h)) + sum(c $ (u(c) = 0 and a(c, l) = 1), delta(c, d, h1)) =l= 1;

const4(j, d, h, h1) $ (g(h) = 1 and g(h1) = 0 and t(h, h1) = 1)..
    sum(c $ (u(c) = 1 and s(j, c) = 1), delta(c, d, h)) + sum(c $ (u(c) = 0 and s(j, c) = 1), delta(c, d, h1)) =l= 1;
    
const5(c, l, d, h) $ (a(c, l) = 1 and u(c) = g(h))..
    delta(c, d, h) =l= b(l, d, h);
    
const6(c, d) $ (n(c) > 1)..
    sum(h $ (u(c) = g(h)), delta(c, d, h)) =l= 1;

* Soft Constraints:

const7..
    sum((c, d, h) $ (f(h) = 1 and u(c) = g(h)), delta(c, d, h)) - w =l= 0;
    
const8(c, d) $ (n(c) > 1 and d.val < last_d.val)..
    sum(h $ (u(c) = g(h)), delta(c, d, h)) + sum(h $ (u(c) = g(h)), delta(c, d + 1, h)) - v(c, d) =l= 1;
    
const9(c, d, h) $ (n(c) > 1 and u(c) = g(h))..
    sum((d1, h1) $ (d.val <> d1.val and h.val <> h1.val and g(h) = g(h1)), delta(c, d1, h1) - (n(c) - 1) * gamma(c)) =l= M * (1 - delta(c, d, h));
   
* Constraints for Mullti-Purpose Model:

const10..
    w =e= opt_z1;
    
const11..
    sum((c, d) $ (n(c) > 1 and d.val < last_d.val), v(c, d)) =e= opt_z2;


model first_soft_course_Timetabling /obj1, const1, const2, const3, const4, const5, const6, const7/;
model second_soft_course_Timetabling /obj2, const1, const2, const3, const4, const5, const6, const7, const8, const10/;
model third_soft_course_Timetabling /obj3, const1, const2, const3, const4, const5, const6, const7, const8, const9, const10, const11/;

solve first_soft_course_Timetabling using MIP minimizing z1;
opt_z1 = z1.l;
display "First Model Solved", z1.l, w.l, delta.l;
*$onText
solve second_soft_course_Timetabling using MIP minimizing z2;
opt_z2 = z2.l;
display "Second Model Solved", z2.l, w.l, v.l, delta.l;

solve third_soft_course_Timetabling using MIP minimizing z3;
display "Third Model Solved", z3.l, v.l, gamma.l, delta.l;
*$offText