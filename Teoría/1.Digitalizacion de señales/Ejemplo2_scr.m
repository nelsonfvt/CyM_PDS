%% Simulación y discretización de uns sitema de segundo orden
%Generando base de tiempo
T=30;
tsim=0.01;
t=0:tsim:T;

%parámetros del sistema
m=30;
b=20;
k=50;

% Constantes de la F. de transferencia
b1=b/m;
a1=b1;
b2=k/m;
a2=b2;
num=[0 b1 b2];
den=[1 b1 b2];

% Simulación: Respuesta escalón del sistema
[y]=step(num,den,t);
figure
plot(t,y)
xlabel('tiempo (segundos)')
ylabel('Amplitud')

%% Muestreo de la Respuesta al escalón
Ns=100;
nTs=t(1:Ns:length(t));
yTs=y(1:Ns:length(y));
fprintf('Periodo de muestreo: %4.2f segundos',nTs(2))
figure
hold on
plot(t,y)
stem(nTs,yTs)
xlabel('tiempo (segundos)')
ylabel('Amplitud')
hold off

% Representación en tiempo discreto
N=length(nTs);
n=0:N-1;
figure
stem(n,yTs)
xlabel('tiempo (muestras)')
ylabel('Amplitud')