syms Thx Thy Thz %Angulos
syms Xpp Ypp Zpp %Aceleraciones
syms g; %Aceleración gravedad
% Otras variables de estado:
syms X Xp Y Yp Z Zp Thxp Thyp Thzp
%Vector de estado
X_s = [X Xp Xpp Y Yp Ypp Z Zp Zpp Thx Thxp Thy Thyp Thz Thzp];

Rx = [1 0 0;
      0 cos(Thx) -sin(Thx);
      0 sin(Thx) cos(Thx)];

Ry = [cos(Thy) 0 sin(Thy);
      0 1 0;
      -sin(Thy) 0 cos(Thy)];
  
Rz = [cos(Thz) -sin(Thz) 0;
      sin(Thz) cos(Thz) 0;
      0 0 1];
  
RT = Rx*Ry*Rz;

As = RT*[Xpp; Ypp; Zpp-g];

H = sym( 'H',[6 15]);

H(4,11) = 1;
H(5,13) = 1;
H(6,15) = 1;

for i=1:6
    for j=1:15
        if i<4
            H(i,j) = diff(As(i),X_s(j));
        else
            H(i,j) = 0;
        end
    
    end
end
