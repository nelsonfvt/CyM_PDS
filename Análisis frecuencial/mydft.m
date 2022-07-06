function [dft] = mydft(seg)
%Calculo de la DFT
%Input
%   deg: señal de tiempo discreto, es un arreglo de N valores reales
%Output
%   dft: DFT de la secuendia de entrada seg, es un arreglo de N valores
%   complejos

N=length(seg);
dft=zeros(size(seg));

for k=1:N
    for j=1:N
        dft(k)=dft(k) + seg(j)*cos((2*pi*(k-1)*(j-1))/N) + 1j*seg(j)*sin((2*pi*(k-1)*(j-1))/N);
    end
end