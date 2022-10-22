function [] = Plot_robot(Angs)
%Plot_robot dibuja el manipulador 3DOF en el espacio
%Input:
%   Arg: vector con tres ángulos (radianes)
a = [0 10 10];

A01 = [cos(Angs(1)) 0 sin(Angs(1)) 0;
       sin(Angs(1)) 0 -cos(Angs(1)) 0;
       0 1 0 0;
       0 0 0 1];
A12 = [cos(Angs(2)) -sin(Angs(2)) 0 a(2)*cos(Angs(2));
       sin(Angs(2)) cos(Angs(2)) 0 a(2)*sin(Angs(2));
       0 0 1 0;
       0 0 0 1];
A23 = [cos(Angs(3)) -sin(Angs(3)) 0 a(3)*cos(Angs(3));
       sin(Angs(3)) cos(Angs(3)) 0 a(3)*sin(Angs(3));
       0 0 1 0;
       0 0 0 1];
   
A02 = A01*A12;   
A03 = A02*A23;
Pcod = A02(1:3,4);
Pfin = A03(1:3,4);
figure()
hold on
plot3([0 Pcod(1)],[0 Pcod(2)],[0 Pcod(3)],'-k','LineWidth',4)
plot3([Pcod(1) Pfin(1)],[Pcod(2) Pfin(2)],[Pcod(3) Pfin(3)],'-m','LineWidth',4)
plot3([0 10], [0 0], [0 0],'--r','LineWidth',1) %eje X
plot3([0 0], [0 10], [0 0],'--b','LineWidth',1) %eje Y
plot3([0 0], [0 0], [0 10],'--g','LineWidth',1) %eje Z
axis equal
axis auto
grid on
hold off
end

