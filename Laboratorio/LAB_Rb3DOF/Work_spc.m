% Simulación espacio de trabajo Robot 3DOF

Angs1 = -pi/3:0.1:pi/6; %rango primera articulación
Angs2 = -pi/3:0.1:pi/3; %rango segunda articulación
Angs3 =  0.01:0.1:2*pi/3; %rango tercera articulación

avec = [];
pvec = [];

%% searching spaces
for i = 1:length(Angs1)
    for j = 1:length(Angs2)
        for k = 1:length(Angs3)
            Ths = [Angs1(i) Angs2(j) Angs3(k)];
            Pos = CDir3DOF(Ths);
            fang = CInv3DOF(Pos);
            % determinar coeherencia entre modelos cinemáticos
            if norm(Ths - fang') <= 0.01
                avec = [avec Ths'];
                pvec = [pvec Pos];
            end
            
        end
    end
end
%% figures
%Work space
figure(1)
hold on
scatter3(pvec(1,:),pvec(2,:),pvec(3,:))
plot3([0 10], [0 0], [0 0],'--r','LineWidth',2) %eje X
plot3([0 0], [0 10], [0 0],'--b','LineWidth',2) %eje Y
plot3([0 0], [0 0], [0 10],'--g','LineWidth',2) %eje Z
axis equal
axis auto
grid on
hold off
%% Configuration examples
[~,Ix] = find(abs(avec(1,:)) < 0.8);
exam = avec(:,Ix);
[~,Ix] = find(abs(exam(2,:)) < 0.5);
exam = exam(:,Ix);
[~,Ix] = find(exam(3,:) > 0.1 & exam(3,:) < 1.5);
exam = exam(:,Ix);
ind = randi([1 length(exam(1,:))]);
Plot_robot(exam(:,ind))
ind = randi([1 length(exam(1,:))]);
Plot_robot(exam(:,ind))
ind = randi([1 length(exam(1,:))]);
Plot_robot(exam(:,ind))