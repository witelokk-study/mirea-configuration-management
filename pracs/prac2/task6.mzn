predicate caret(var int: package, int: ver) = (package >= ver /\ package < ((ver / 100 + 1)*100));

set of int: FOO = {100, 110};
set of int: TARGET = {100, 200};
set of int: LEFT = {100};
set of int: RIGHT = {100};
set of int: SHARED = {100, 200};

int: root = 100;
var FOO: foo;
var TARGET: target;
var LEFT: left;
var RIGHT: right;
var SHARED: shared;

constraint root == 100 <- caret(foo, 100) /\ caret(target, 200);
constraint foo == 110 <- caret(left, 100) /\ caret(right, 100);
constraint left == 100 <- shared >= 100;
constraint right == 100 <- shared < 200;
constraint shared == 100 <- caret(target, 100);

solve maximize(sum([foo, target]))
