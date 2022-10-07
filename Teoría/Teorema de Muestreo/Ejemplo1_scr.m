% Señal de tiempo continuo
t=0:0.001:1;
xt=2*cos(2*pi*2*t)+3*sin(2*pi*6*t); % 2 Hz y 6 Hz
figure,
plot(t,xt)
hold on
% Discretización de la señal análoga
Ts=1/18; % Periodo de muestreo
Fs=1/Ts;
nT=0:Ts:1;
xnT=2*cos(2*pi*2*nT)+3*sin(2*pi*6*nT);
stem(nT,xnT)
hold off 
N=Fs;
% Señal de tiempo discreto
n=0:N; % la variable de tiempo es discreta, valores enteros
xn=2*cos(2*pi*(2/Fs)*n)+3*sin(2*pi*(6/Fs)*n);
figure,
stem(n,xn)
