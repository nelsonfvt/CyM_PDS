% Señal de tiempo continuo
t=0:0.001:1;
f1 = 4;
f2 = 6;
xt=2*cos(2*pi*f1*t)+3*sin(2*pi*f2*t); % 4 Hz y 6 Hz
figure,
plot(t,xt)
hold on
% Discretización de la señal análoga
Ts=1/24; % Periodo de muestreo
Fs=1/Ts;
nT=0:Ts:1;
xnT=2*cos(2*pi*f1*nT)+3*sin(2*pi*f2*nT);
stem(nT,xnT)
xlabel('tiempo (segundos)')
ylabel('Amplitud')
hold off 
N=Fs;
% Señal de tiempo discreto
n=0:N-1; % la variable de tiempo es discreta, valores enteros
xn=2*cos(2*pi*(f1/Fs)*n)+3*sin(2*pi*(f2/Fs)*n);
figure,
stem(n,xn)
