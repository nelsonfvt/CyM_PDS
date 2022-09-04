function [EF]=Dir_model(T)
%Dir_model: Modelo cinemático directo brazo antropomorfico 3DOF
%Input
%   T: vector con ángulos de articulación (radianes)
%Output
%   EF: Posición del efector final desde hombro

 P = [0; 0; 0; 1];

 a = [0 10 10];

 A01 = [cos(T(1)) 0 sin(T(1)) 0;
        sin(T(1)) 0 -cos(T(1)) 0;
        0 1 0 0;
        0 0 0 1];

  A12 = [cos(T(2)) -sin(T(2)) 0 a(2)*cos(T(2));
         sin(T(2)) cos(T(2)) 0 a(2)*sin(T(2));
         0 0 1 0;
         0 0 0 1];
  A23 = [cos(T(3)) -sin(T(3)) 0 a(3)*cos(T(3));
         sin(T(3)) cos(T(3)) 0 a(3)*sin(T(3));
         0 0 1 0;
         0 0 0 1];
     
  A03 = A01*A12*A23;
  
  EF = A03*P;
end