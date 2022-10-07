function circulo(x,y,r)
% Funcion para dibujar un circulo en coordenadas x,y de radio r

ang=0:0.01:2*pi; 
xp=r*cos(ang);
yp=r*sin(ang);
plot(x+xp,y+yp)
end

