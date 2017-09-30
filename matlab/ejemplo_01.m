clear;clc;close all;
hold on; % Mantener gráficos
a = 4; % Longitud de la caja sobre el eje u
b = 2; % Longitud de la caja sobre el eje v
c = 1; % Longitud de la caja sobre el eje w
O = [0,0,0,1]'; % Coordenadas locales homogéneas del origen.

alpha = pi; % Ángulo a rotar
q = [5,0,5]; % Vector de traslación

% Ejes coordenados locales
plot3([0,1],[0,0],[0,0],'r-*','linewidth',2);
plot3([0,0],[0,1],[0,0],'b-*','linewidth',2);
plot3([0,0],[0,0],[0,1],'g-*','linewidth',2);

% Puntos de la caja en coordenadas locales homogéneas
A = [0,0,0,1]';
B = [0,b,0,1]';
C = [0,b,c,1]';
D = [0,0,c,1]';
E = [a,0,0,1]';
F = [a,b,0,1]';
G = [a,b,c,1]';
H = [a,0,c,1]';

drawbox(A,B,C,D,E,F,G,H, 0.8*ones(1,3));

M = mthtras(q)*mthrz(alpha); % Matriz de transformación 
A = M*A; % Transformación de las coordenadas de cada punto
B = M*B;
C = M*C;
D = M*D;
E = M*E;
F = M*F;
G = M*G;
H = M*H;

drawbox(A,B,C,D,E,F,G,H, 0.9*ones(1,3));

% Para dibujar el marco de referencia transformado
u = M(1:3,1);
v = M(1:3,2);
w = M(1:3,3);
Ouvw = M(1:3,4);

plot3([Ouvw(1),Ouvw(1)+u(1)],[Ouvw(2),Ouvw(2)+u(2)],[Ouvw(3),Ouvw(3)+u(3)],'r-*','linewidth',3);
plot3([Ouvw(1),Ouvw(1)+v(1)],[Ouvw(2),Ouvw(2)+v(2)],[Ouvw(3),Ouvw(3)+v(3)],'b-*','linewidth',3);
plot3([Ouvw(1),Ouvw(1)+w(1)],[Ouvw(2),Ouvw(2)+w(2)],[Ouvw(3),Ouvw(3)+w(3)],'g-*','linewidth',3);

view([10,10,10]);
axis([-20,20,-20,20,-20,20]);
grid('on');