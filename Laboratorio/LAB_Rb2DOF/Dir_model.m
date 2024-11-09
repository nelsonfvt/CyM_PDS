function [Pfin] = Dir_model(Angs)
%Dir_model Modelo cinemático directo 2DOF
%   función que calcula la posición final de un manipulador planar
%   de 2 grados de libertad (2DOF).
%   Los parámteros de entrada son los ángulos de las articulaciones
%   La salida corresponde a la posición del extremo final del brazo
%Input:
%   Angs: vector 2x1 con valores de ángulos en radianes
%Output:
%   Pfin: vector 2x1 con coordenadas cartesianas del extremo final del
%   brazo
a = [10 10]; %Longitudes de eslabones
d = [0 0];
al = [0 0];

% Matrices de transformacion homogenea
A01 = Mx_hgne(a(1), d(1),al(1),Angs(1));
A12 = Mx_hgne(a(2), d(2),al(2),Angs(2));

%Matriz final
A02 = A01*A12;

%Posicion punto final del brazo
Pfin = A02(1:2,4);

end

function [Mx] = Mx_hgne(a,d,al,T)
    Mx = [cos(T) -sin(T)*cos(al) sin(T)*cos(al) a*cos(T);
          sin(T) cos(T)*cos(al) -sin(T)*cos(al) a*sin(T);
          0 sin(al) cos(al) d;
          0 0 0 1];
end