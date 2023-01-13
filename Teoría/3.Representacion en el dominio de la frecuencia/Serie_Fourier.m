%% Primera parte
% crear senal a partir de sinusoidales

prompt = "Ingrese el numero de armonicos: ";
N = input(prompt);
prompt = "Ingrese la frecuencia base de la senal a reconstruir: ";
F = input(prompt);
prompt = "Ingrese el nivel DC de la senal a reconstruir: ";
D = input(prompt);

Nc = 10; %representar Nc ciclos de la senal
t = 0 : 1/(F*4*N) : Nc/F;

ft = ones(1,length(t))*D; % Aplicando nivel DC
for n=1:N % Combinando N armonicos de amplitud 1
    ft = ft + cos(2*pi*n*F*t) - sin(2*pi*n*F*t);
end

figure
plot(t,ft)
xlabel('Tiempo (segundos)')
ylabel('Amplitud')

%% Segunda parte
% espectro de frecuencia

% xk = abs(fft(ft)) / length(t);
% xk = xk(1:floor(length(t) / 2));
% f = (0:length(xk)-1) / length(xk);
% f = f * (N*F*2);
% figure
% stem(f,xk)
% xlabel('Frecuencia (Hz)')
% ylabel('Magnitud del espectro')