%Parámetros
F = 50; %frecuencia señal de tiempo continuo
Fs = 500; %frecuencia de muestreo
f = F/Fs; %frecuencia normalizada (muestras/ciclo)
Tf = 0.05; %tiempo de simulación
fa = 0; % fase

% Señal de tiempo continuo
t = 0:0.00001:Tf;
xt = 1.5*cos(2*pi*F*t + fa) + 1.5;

%Señal de tiempo discreto
nt = 0:1/Fs:Tf;
xnt = 1.5*cos(2*pi*F*nt + fa) + 1.5;

%Gráficas
figure,
hold on
plot(t,xt)
stem(nt,xnt)

