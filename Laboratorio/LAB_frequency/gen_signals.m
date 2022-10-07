Ac_x = 0.1*randn(10000,1);
Ac_y = 0.15*randn(10000,1);
Ac_z = 9.8 + 0.13*randn(10000,1);

Gy_x = 0.1*randn(10000,1);
Gy_y = 0.1*randn(10000,1);
Gy_z = 0.1*randn(10000,1);

csvwrite('static.csv',[Ac_x Ac_y Ac_z Gy_x Gy_y Gy_z]);

Ac_x = 0.1*randn(1,10000);
Ac_y = 0.15*randn(1,10000);
Ac_z = 7 + 0.13*randn(1,10000);

Gy_x = 0.2*randn(1,10000);
Gy_y = 0.2*randn(1,10000);
Gy_z = 0.2*randn(1,10000);

n = 0:9999;

N_ar = 10;
f = 1:N_ar;
a = rand(6,N_ar)*0.7;
b = rand(6,N_ar)*0.7;

for i=1:N_ar
    Ac_x = Ac_x + a(1,i)*cos(2*pi*n*(f(i)/200)) + b(1,i)*sin(2*pi*n*(f(i)/200));
    Ac_y = Ac_y + a(2,i)*cos(2*pi*n*(f(i)/200)) + b(2,i)*sin(2*pi*n*(f(i)/200));
    Ac_z = Ac_z + a(3,i)*cos(2*pi*n*(f(i)/200)) + b(3,i)*sin(2*pi*n*(f(i)/200));
    
    Gy_x = Gy_x + a(4,i)*cos(2*pi*n*(f(i)/200)) + b(4,i)*sin(2*pi*n*(f(i)/200));
    Gy_y = Gy_y + a(5,i)*cos(2*pi*n*(f(i)/200)) - b(5,i)*sin(2*pi*n*(f(i)/200));
    Gy_z = Gy_z - a(6,i)*cos(2*pi*n*(f(i)/200)) + b(6,i)*sin(2*pi*n*(f(i)/200));
end

csvwrite('motion.csv',[Ac_x' Ac_y' Ac_z' Gy_x' Gy_y' Gy_z']);