function [dLP] = dLogP_xth(x,th)
%Función que calcula la derivada de Log likelihood de x dado theta
%   x: corresponde a las observaciones (vector)
%   th: es el parámetro que se desea conocer
%   Para el ejemplo se sabe que la varianza es 1
var=1;
m_b=mean(x);
n=length(x);
dLP = -2*(m_b-th)/(2*var^2);
end
