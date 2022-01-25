%señal exponencial real
n= 0:9;
A=-0.5;
xn=A.^n;
stem(n,xn)

%Señal exponencial compleja
n= 0:9;
A=0.5+0.5*i;
xn=A.^n;
figure('Name','Parte real')
stem(n,real(xn))
figure('Name','Parte imaginaria')
stem(n,imag(xn))
