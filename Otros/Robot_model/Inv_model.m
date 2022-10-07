function [T] = Inv_model(EF)
%Inv_model Modelo cinemático inverso brazo antropomorfico 3DOF
%Input
%   EF: vector posiciones del efector final (x, y, z) desde hombro
%Output:
%   T: ángulos de articulación (radianes)

T=[0 0 0];
a = [0 10 10];

T(1) = atan2(EF(2),EF(1));

c3 = (EF(1)^2 + EF(2)^2 + EF(3)^2 -a(2)^2 -a(3)^2 )/(2*a(2)*a(3));
s3 = sqrt(1-c3^2);
T(3) = atan2(s3,c3);

s2 = ((a(2)+a(3)*c3)*EF(3) - a(3)*s3*sqrt(EF(1)^2 + EF(2)^2)) / (EF(1)^2 + EF(2)^2 + EF(3)^2);
c2 = ( (a(2)+a(3)*c3)*sqrt(EF(1)^2 + EF(2)^2) + a(3)*s3*EF(3) ) / (EF(1)^2 + EF(2)^2 + EF(3)^2);
T(2) = atan2(s2,c2);
end