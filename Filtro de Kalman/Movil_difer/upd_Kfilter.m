function [xt_t,Pt_t,y_t] = upd_Kfilter(xt,z,Pt,Kfil_str)
%UPD_KFILTER Etapa de actualizacion del filtro de Kalman
%
%INPUT:
%   xt: vector prediccion de estados
%   z: vector de lectura de sensores
%
%   Kfil_str: estructura con las matrices del sistema
%       F: Matriz de transición del sistema
%       B: Matriz de entrada del sistema
%       P: Matriz de covarianza de prediccion
%       H: Matriz de observacion
%       Q: covarianza del ruido del sistema
%       R: covarianza de los sensores
%OUTPUT:
%   xt_t: vector estados corregidos
%   Pt_t: Matriz prediccion covarianza corregida
%   y_t: vector error final de sensores

F=Kfil_str.F;
R=Kfil_str.R;
H=Kfil_str.H;

y= z-H*xt;
S=H*Pt*H'+R;
K=Pt*H'*S^(-1);
xt_t = xt+K*y;
KH=K*H;
[n,~]=size(KH);
Pt_t=(eye(n)-KH)*Pt;
y_t=z-H*xt_t;
end

