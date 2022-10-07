function [Angs] = CInv3DOF(Pfin)
%CInv3DOF Modelo cinemático inverso 3DOF
%   Cálculo de los ángulos para un robot antropomórfico de 3 grados de
%   libertad a partir de la posición final dele extremo del robot
%Input:
%   Pfin: vector 3x1 con coordenadas cartesianas
%Output:
%   Angs: vector 3x1 con ángulos en radianes
Angs = zeros(3,1);
a = [0 10 10];

Angs(1) = atan2(Pfin(2),Pfin(1));

c3 = (Pfin(1)^2 + Pfin(2)^2 + Pfin(3)^2 -a(2)^2 -a(3)^2 )/(2*a(2)*a(3));
s3 = sqrt(1-c3^2);

Angs(3) = atan2(s3,c3);

s2 = ((a(2)+a(3)*c3)*Pfin(3) - a(3)*s3*sqrt(Pfin(1)^2 + Pfin(2)^2)) / (Pfin(1)^2 + Pfin(2)^2 + Pfin(3)^2);
c2 = ( (a(2)+a(3)*c3)*sqrt(Pfin(1)^2 + Pfin(2)^2) + a(3)*s3*Pfin(3) ) / (Pfin(1)^2 + Pfin(2)^2 + Pfin(3)^2);

Angs(2) = atan2(s2,c2);
end