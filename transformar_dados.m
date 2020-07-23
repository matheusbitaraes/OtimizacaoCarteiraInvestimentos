load previsoes.mat

valorizacao = previsoes(365,:)./previsoes(1,:);

carteira = csvread('nsgaII.py/otm.csv', 2, 0);
