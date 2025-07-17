function [xt,Pt] = pred_Kfilter(x,u,Kfil_str)
%PRED_KFILTER Etapa de prediccion del filtro de Kalman
%
%INPUT:
%   x: vector de estados actuales del sistema
%   u: vector de entradas del sistema
%   
%   Kfil_str: estructura con las matrices del sistema
%       F: Matriz de transición del sistema
%       B: Matriz de entrada del sistema
%       P: Matriz de covarianza de prediccion
%       Q: covarianza del ruido del sistema
%       R: covarianza de los sensores
%OUTPUT:
%   xt: vector prediccion de estados
%   Pt: Matriz prediccion covarianza
F=Kfil_str.F;
B=Kfil_str.B;
Q=Kfil_str.Q;
P=Kfil_str.P;

xt = F*x + B*u;
Pt = F*P*F' + Q;
end

