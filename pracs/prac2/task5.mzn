var {100, 110, 120, 130, 140, 150}: menu;
var {180, 200, 210, 220, 230}: dropdown;
var {100, 200}: icons;

constraint icons == 100;
constraint menu == 100 <- dropdown == 180;
constraint menu >= 110 <- dropdown >= 200;