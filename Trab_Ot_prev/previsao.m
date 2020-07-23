ABEV3 = xlsread('c:\Eng Gustavo Vinicius\MATERIAL_DOUTORADO_UFMG\dados_historicos.xlsx', 2, 'B3:B1240');

y = ABEV3;

T = length(y);


Md1 = arima(13,0,1);

%Md1 = arima('Constant',4,'D',1,'Seasonality',0,'MALags',1,'SMALags',1);

%Mdl = arima('Constant',0,'D',1,'Seasonality',12,...
 %   'MALags',1,'SMALags',12);


EstMd1 = estimate(Md1,y);

K = 360;

[yF,yMSE] = forecast(EstMd1,K,'Y0',y);

upper = yF + 1.96*sqrt(yMSE);

lower = yF - 1.96*sqrt(yMSE);

figure

plot(y,'Color',[.75,.75,.75])

hold on

h1 = plot(T+1:T+360,yF,'r', 'LineWidth',2);

h2 = plot(T+1:T+360, upper, 'k--', 'Linewidth', 1.5);

plot(T+1:T+360,lower, 'k--', 'LineWidth', 1.5)

xlim([0,T+360])

title('Previsão e Intervalo de Previsão de 95%')

hold off

rng 'default';
res = infer(EstMd1,y);
Ysim = simulate(EstMd1,360,'NumPaths',500,'Y0',y,'E0',res);

yBar = mean(Ysim,2);
simU = prctile(Ysim,97.5,2);
simL = prctile(Ysim,2.5,2);

figure
h1 = plot(yF,'Color',[.85,.85,.85],'LineWidth',5);
hold on
h2 = plot(yBar,'k--','LineWidth',1.5);
xlim([0,360])
plot([upper,lower],'Color',[.85,.85,.85],'LineWidth',5)
plot([simU,simL],'k--','LineWidth',1.5)
title('Comparison of MMSE and Monte Carlo Forecasts')
legend([h1,h2],'MMSE','Monte Carlo','Location','NorthWest')
hold off    