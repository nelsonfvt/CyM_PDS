function [Pfin] = CDir3DOF(Angs)
%CDir3DOF Modelo cinemático directo 3DOF
%   función que calcula la posición final de un manipulador antropormórfico
%   de 3 grados de libertad (3DOF).
%   Los parámteros de entrada son los ángulos de las articulaciones
%   La salida corresponde a la posición del estremo final del brazo
%Input:
%   Angs: vector 3x1 con valores de ángulos en radianes
%Output:
%   Pfin: vector 3x1 con coordenadas cartesianas del extremo final del
%   brazo

a = [0 10 10];
d = [0 0 0];
al = [pi/2 0 0];

A01 = Mx_hgne(a(1), d(1),al(1),Angs(1));
A12 = Mx_hgne(a(2), d(2),al(2),Angs(2));
A23 = Mx_hgne(a(3), d(3),al(3),Angs(3));

A03 = A01*A12*A23;

Pfin = A03(1:3,4);
end

function [Mx] = Mx_hgne(a,d,al,T)
    Mx = [cos(T) -sin(T)*cos(al) sin(T)*cos(al) a*cos(T);
          sin(T) cos(T)*cos(al) -sin(T)*cos(al) a*sin(T);
          0 sin(al) cos(al) d;
          0 0 0 1];
end