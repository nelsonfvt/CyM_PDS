%Parámetros
F = 50; %frecuencia señal de tiempo continuo
Fs = 500; %frecuencia de muestreo
Tf = 0.05; %tiempo de simulación
fa = 0; % fase (radianes)

% Señal de tiempo continuo
t = 0:0.00001:Tf;
xt = 1.5*cos(2*pi*F*t + fa) + 1.6;

%Señal de tiempo discreto
nt = 0:1/Fs:Tf;
xnt = 1.5*cos(2*pi*F*nt + fa) + 1.6;

%Gráficas
figure('Name','Señal análoga y señal discretizada')
xlabel('Tiempo (segundos)')
ylabel('Voltaje (V)')
hold on
plot(t,xt)
stem(nt,xnt)
hold off