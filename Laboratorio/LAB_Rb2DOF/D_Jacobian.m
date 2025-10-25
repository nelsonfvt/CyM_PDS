function [J_a] = D_Jacobian(q,l)
%D_Jacobian Jacobiano del robot
%   Calculo del Jacobiano del robot planar 2DOF
%Input:
%   q: vector con posiciones articulares
%   l: vector con longitudes de eslabones
%Output:
%   J_a: Matriz Jacobiana 2x2

J_a = [-l(1)*sin(q(1))-l(2)*sin(q(1)+q(2)) -l(2)*sin(q(1)+q(2));
    l(1)*cos(q(1))+l(2)*cos(q(1)+q(2)) l(2)*cos(q(1)+q(2))];
end