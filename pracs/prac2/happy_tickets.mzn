include "alldifferent.mzn";

var 0..9: A;
var 0..9: B;
var 0..9: C;
var 0..9: D;
var 0..9: E;
var 0..9: F;

constraint alldifferent([A,B,C,D,E,F]);

constraint A+B+C = D+E+F;

solve satisfy;