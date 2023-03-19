function [] = Plot_robot(Angs)
%Plot_robot dibuja el manipulador 3DOF en el espacio
%Input:
%   Arg: vector con tres ángulos (radianes)
a = [0 10 10];
d = [0 0 0];
al = [pi/2 0 0];

A01 = Mx_hgne(a(1), d(1),al(1),Angs(1));
A12 = Mx_hgne(a(2), d(2),al(2),Angs(2));
A23 = Mx_hgne(a(3), d(3),al(3),Angs(3));
   
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

function [Mx] = Mx_hgne(a,d,al,T)
    Mx = [cos(T) -sin(T)*cos(al) sin(T)*cos(al) a*cos(T);
          sin(T) cos(T)*cos(al) -sin(T)*cos(al) a*sin(T);
          0 sin(al) cos(al) d;
          0 0 0 1];
end
