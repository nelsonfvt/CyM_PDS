% Simulación espacio de trabajo Robot 3DOF

Angs = -2*pi/3:0.01:2*pi/3;

avec = [];
pvec = [];

for i = 1:length(Angs)
    for j = 1:length(Angs)
        for k = 1:length(Angs)
            Ths = [Angs(i) Angs(j) Angs(k)];
            Pos = CDir3DOF(Ths);
            fang = CInv3DOF(Pos);
            
            if norm(Ths - fang') <= 0.01
                avec = [avec Ths'];
                pvec = [pvec Pos'];
            end
            
        end
    end
end