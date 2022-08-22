function [v_r] = dk_model (wl,wr,r,l)
%INPUT:
%   r radio de las ruedas en metros
%   l distancia de las ruedas al centro del robot en metros
%   wl velocidad angular de la rueda izquierda en rad/s
%   wr velocidad angular de la rueda derecha en rad/s
%OUTPUT:
%   v_r vector de velocidades del chasis

ph=[wr;wl];
Mx=[r/2 r/2;
    0 0;
   r/(2*l) -r/(2*l)];

v_r=Mx*ph;
end
