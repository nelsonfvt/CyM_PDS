%Simulación de un robot movil y uso del filtro de Kalman
dt=0.001;
t=0:dt:10;
N=length(t);

%dimensiones robot
r=0.025; %diametro ruedas
l=0.2; %distancia rueda-centro de masa

%velocidades angulares de las ruedas
wr=16*pi*ones(size(t)); %rad/s
wl=wr; %rad/s
pt1 = round(N/3);
pt2 = round(2*N/3);
l1=100;
l2=200;
wl(pt1:pt1+l1)=wl(pt1:pt1+l1)*0.1;
wr(pt2:pt2+l2)=wr(pt2:pt2+l2)*0.2;
th_0=0; %angulo inicial
Ps_0=[0;0]; %posición inicial

%inicializando vector de posicion
Ps_t=zeros(3,N);
Ps_t(:,1)=[Ps_0;th_0];

% DESPLAZAMIENTO IDEAL DEL ROBOT
V_R=zeros(3,N); %[Vx;Vy=0;W] desde el chasis
V_I=zeros(3,N); %[Vx;Vy;W] desde sistema global
for i=2:N
  V_ch=dk_model(wl(i-1),wr(i-1),r,l); %calculo velocidades del chasis
  V_sg=d_Rotac(V_ch,Ps_t(3,i-1)); % calculo velocidades desde sistema global
  Ps_t(:,i)=Ps_t(:,i-1)+(V_sg.*dt);% calculo posicion y orientacion del robot
  V_R(:,i)=V_ch;
  V_I(:,i)=V_sg;
end

% Modelo sistema KALMAN
F=[1 dt 0 0;
   -1/dt 0 0 0;
   0 0 1 dt;
   0 0 0 0];
B=[0 0;
   1/dt 0
   0 0;
   0 1];

% Modelo sensor KALMAN
H=[0 1 0 0;
   0 0 0 1];

% Matrices de Covarianza KALMAN
Q=[0.1 0 0 0;
   0 0.1 0 0;
   0 0 0.1 0;
   0 0 0 0.1];
R=[0.2 0;
   0 0.2];
P=[0.8 0 0 0;
   0 0.8 0 0;
   0 0 0.8 0;
   0 0 0 0.8];

%Estructura con matrices para filtro Kalman
k_fil.F=F;
k_fil.B=B;
k_fil.H=H;
k_fil.Q=Q;
k_fil.R=R;
k_fil.P=P;

%adicion de  ruido a velocidades del robot = velociades reales
wl_n=wl+randn(1,N)*0.1; %rueda izq
wr_n=wr+randn(1,N)*0.1; %rueda der
V_Rn=zeros(3,N); % desde chasis
V_In=zeros(3,N); % desde sistema global

Ps_tn=zeros(3,N); % posicion y orientacion real
Ps_tn(:,1)=[Ps_0;th_0];

Ps_ts=zeros(3,N); % posicion y orientacion segun sensor
Ps_ts(:,1)=[Ps_0;th_0];

Ps_tk=zeros(3,N); % posiscion y orientacion filtradas
Ps_tk(:,1)=[Ps_0;th_0];


xt=[0;0;th_0;0]; % estados iniciales (vel lin, Ac lin, ang, vel ang)
z_1=[0;0]; %lectura sensor (t-1)
c=[0;0];
for i=2:N
  
  % TRAYECTORIA REAL DEL ROBOT
  V_Rn(:,i)=dk_model(wl_n(i-1),wr_n(i-1),r,l);
  V_In(:,i)=d_Rotac(V_Rn(:,i),Ps_tn(3,i-1)); %velocidades respecto a sistema global reales
  Ps_tn(:,i)=Ps_tn(:,i-1)+(V_In(:,i).*dt); %posicion y orientacion reales del robot
  
  % CALCULO LECTURA DE SENSOR IDEAL
  z_i=[(V_Rn(1,i) - V_Rn(1,i-1))/dt; % acelearcion vista por sensor sin ruido
        V_Rn(3,i)]; % velocidad angular vista por sensor sin ruido
  
  % FILTRO DE KALMAN
  u = [V_R(1,i);V_R(3,i)]; %entrada del sistema (vel lin, vel ang)
  z = z_i + randn(2,1)*0.2; % lectura sensores + ruido = SENSOR REAL
  [xt,Pt]= pred_Kfilter(xt,u,k_fil); % PEDICCION
  [xt_t,Pt_t,e] = upd_Kfilter(xt,z,Pt,k_fil); % ACTUALIZACION
  k_fil.P=Pt_t; % actualizar covarianza
  xt=xt_t; % actualizar estados
  V_Ik=d_Rotac([xt(1);0;xt(4)],xt(3));
  Ps_tk(:,i)=Ps_tk(:,i-1)+(V_Ik .*dt); % posicion y orientacion segun KALMAN
  
  % CALCULO POSICION SEGUN SENSORES
  V_c=c(1) + (dt/2 * (z_1(1) + z(1))); % integrando aceleracion: metodo del trapecio
  An_c=c(2) + (dt/2 * (z_1(2) + z(2))); % integrando vel_ang: metodo trapecio
  Vc = d_Rotac([V_c;0;z(2)],An_c);
  Ps_ts(:,i)=Ps_ts(:,i-1)+(Vc.*dt); % posicion y orientacion segun sensores
  z_1=[z(1);z(2)];
  c=[V_c;An_c];
end

figure(1)
subplot(2,3,1)
hold on
scatter(Ps_t(1,:),Ps_t(2,:),'.')
scatter(Ps_tn(1,:),Ps_tn(2,:),'.')
legend('ideal','real')
title('Recorrido ideal vs real')
xlabel('eje X (m)')
ylabel('eje Y (m)')
hold off

subplot(2,3,2)
hold on
scatter(Ps_tn(1,:),Ps_tn(2,:),'.')
scatter(Ps_ts(1,:),Ps_ts(2,:),'.')
legend('real','medido')
title('Recorrido real vs medido')
xlabel('eje X (m)')
ylabel('eje Y (m)')
hold off

subplot(2,3,3)
hold on
scatter(Ps_tn(1,:),Ps_tn(2,:),'.')
scatter(Ps_tk(1,:),Ps_tk(2,:),'.')
legend('real','filtrado')
title('Recorrido real vs filtrado')
xlabel('eje X (m)')
ylabel('eje Y (m)')
hold off

e_i=Ps_t-Ps_tn;
y1=((e_i(1,:)-e_i(2,:)).^2).^0.5;
e_s=Ps_tn-Ps_ts;
y2=((e_s(1,:)-e_s(2,:)).^2).^0.5;
e_k=Ps_tn-Ps_tk;
y3=((e_k(1,:)-e_k(2,:)).^2).^0.5;


subplot(2,3,4)
hold on
scatter(t,y1,'.')
scatter(t,abs(e_i(3,:)),'.')
legend('Err pos','Err orient')
title('Error real')
xlabel('tiempo (s)')
ylabel('Error')
hold off

subplot(2,3,5)
hold on
scatter(t,y2,'.')
scatter(t,abs(e_s(3,:)),'.')
legend('Err pos','Err orient')
title('Error sensado')
xlabel('tiempo (s)')
ylabel('Error')
hold off

subplot(2,3,6)
hold on
scatter(t,y3,'.')
scatter(t,abs(e_k(3,:)),'.')
legend('Err pos','Err orient')
title('Error Kalman')
xlabel('tiempo (s)')
ylabel('Error')
hold off