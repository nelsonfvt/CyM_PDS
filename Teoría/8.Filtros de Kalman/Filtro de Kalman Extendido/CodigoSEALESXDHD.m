% Dimensiones del robot en metros
l=0.2; % distancia centro del robot - rueda
r=0.05; % radio de la rueda
ri=0.05; % distancia centro del robot - IMU

% Periodo de muestreo
ts=1/100; %segundos

% Velocidades angulares de las ruedas
wr=pi; %derecha - rad/seg
wl=0.5*pi; %izquierda - rad/seg

% Postura inicial del robot
theta=pi/3; %orientacion - radianes
X=0; %posicion - metros
Y=0;
% Velocidades iniciales del robot
x_punto=0;
y_punto=0;
theta_punto=0;

X_vec=zeros(1,1000);
Y_vec=zeros(1,1000);

%Matriz Q

Q=[2.500000000000000e-09 5.000000000000001e-07 0 0 0 0;
   5.000000000000001e-07 1.000000000000000e-04 0 0 0 0;
   0 0 2.500000000000000e-09 5.000000000000001e-07 0 0;
   0 0 5.000000000000001e-07 1.000000000000000e-04 0 0;
   0 0 0 0 2.500000000000000e-09 5.000000000000001e-07;
   0 0 0 0 5.000000000000001e-07 1.000000000000000e-04];

%Matriz R
 R= eye(5)*0.1;

%Matriz P
P=eye(6)*0.1;

%Vector de estados
estados = [X;
            x_punto;
            Y;
            y_punto;
            theta;
            theta_punto];

% Simulacion 10 segundos
for i=1:1000
    % atrasos de los estados
    x_p_n1=estados(2);
    y_p_n1=estados(4);
    theta_p_n1=estados(6);

    % PREDICT
    % Calculo de velocidades del chasis
    V=r/2*(wr+wl);
    estados(6)=r/(2*l)*(wr-wl);

    % Calculo de velocidades desde sistema de referencia global
    estados(2)=V*cos(estados(5));
    estados(4)=V*sin(estados(5));

    % Calculo orientacion del robot
    estados(5)=estados(6)*ts+estados(5);
    % Actualizando posicion del robot
    estados(1)=estados(2)*ts+estados(1);
    estados(3)=estados(4)*ts+estados(3);

    % Matriz_F - Jacobiano
    F=[1 ts 0 0 0 0;
       0 0 0 0 sin(estados(5))*(r/2)*(wr+wl) 0;
       0 0 1 ts 0 0;
       0 0 0 0 cos(estados(5))*(r/2)*(wr+wl) 0;
       0 0 0 0 1 ts;
       0 0 0 0 0 1];

    %Actualizacion matriz P
    P=F*P*F'+Q;

    % UPDATE
    %Calculo hx
    A_x=(estados(2)-x_p_n1)/ts;
    A_y=((estados(6)-theta_p_n1)/ts)*ri;
    E_l=(sqrt(estados(2)^2+estados(4)^2)-estados(6)*l)/r;
    E_r=(sqrt(estados(2)^2+estados(4)^2)+estados(6)*l)/r;
    W_z=estados(6);

    hx = [A_x;
          A_y;
          E_l;
          E_r;
          W_z];

    %Comparacion con sensores - calculo y_m
    %Capturar sensores en el vector z
    z = zeros(5,1);
    y_m = z - hx;
    
    %___________________
    %Matriz H

    H=[0 1/ts 0 0 0 0;
       0 0 0 0 0 ri/ts;
       0 estados(2)/(sqrt(estados(2)^2+estados(4)^2)*r) 0 -estados(4)/(sqrt(estados(2)^2+estados(4)^2)*r) 0 l/r;
       0 estados(2)/(sqrt(estados(2)^2+estados(4)^2)*r) 0 -estados(4)/(sqrt(estados(2)^2+estados(4)^2)*r) 0 -l/r;
       0 0 0 0 0 1];

    % Calculo de ganacia de Kalman - K
    S = H*P*H' + R;
    K = (P*H')/S;


    % Ajuste de los estados
    estados = estados + K*y_m;

    % Ajuste Matriz P

    P = (eye(6) - K*H)*P;

    % Almacena datos
    X_vec(i)=estados(1);
    Y_vec(i)=estados(3);
end

% Visualizacion de trayectoria
figure()
scatter(X_vec,Y_vec)
grid on
xlim([-2 2])
ylim([-2 2])