function [vecr] = d_Rotac (vec,th)
%INPUT:
%   vec: vector de veliciades del chasis
%   th: angulo del chasis respecto del sistema global
%OUTPUT:
%   vecr: vector de velocidades del chasis respecto al sistema global
  R_i=[cos(th) -sin(th) 0;
       sin(th) cos(th) 0;
       0 0 1];
  vecr=R_i*vec;
end
