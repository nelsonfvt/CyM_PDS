function [Angs] = Inv_model(Pfin)
%INV_MODEL Modelo cinemático inverso 2DOF
%   Cálculo de los ángulos para un brazo planaro de 2 grados de
%   libertad a partir de la posición final dele extremo del robot
%Input:
%   Pfin: vector 2x1 con coordenadas cartesianas
%Output:
%   Angs: vector 2x1 con ángulos en radianes

Angs = zeros(2,1);
a = [10 10];

c2 = ( Pfin(1)^2 + Pfin(2)^2 - a(1)^2 - a(2)^2 ) / (2*a(1)*a(2));
Angs(2) = acos(c2);

alf = atan2(Pfin(2),Pfin(1));
bet = acos( (a(1) + a(2)*c2) / sqrt( Pfin(1)^2 + Pfin(2)^2 ) );

Angs(1) = alf-bet;
end

