function [Pfin] = CDir3DOF(Angs)
%CDir3DOF Modelo cinemático directo 3DOF
%   función que calcula la posición final de un manipulador antropormórfico
%   de 3 grados de libertad (3DOF).
%   Los parámteros de entrada son los ángulos de las articulaciones
%   La salida corresponde a la posición del estremo final del brazo
%Input:
%   Angs: vector 3x1 con valores de nagulos en radianes
%Output:
%   Pfin: vector 3x1 con coordenadas cartesianas del extremo final del
%   brazo

l = [1 1 1];
a = [0 0 0];
d = [1 1 1];

A01 = [];
A12 = [];
A13 = [];

A03 = A01*A12*A13;

Pfin = A03(1:3,4);
end

