% leitura do arquivo de dados
ativos_series_temporais = csvread('ativos_series_temporais.csv',1,0);
K = 365; % dias
previsoes = zeros(K, size(ativos_series_temporais, 2));

for i = 1 : size(ativos_series_temporais, 2)
    serie_temporal = ativos_series_temporais(:, i);
    
    % retira zeros do final
    serie_temporal = serie_temporal(find(serie_temporal>0));
    
    % gera valores da serie temporal
    [EstMdl,EstParamCov,logL,info] = carteira_func(serie_temporal);

    [yF,yMSE] = forecast(EstMd1,K,'Y0',carteira_func);

%     rng 'default';
%     res = infer(EstMd1,serie_temporal);
%     Ysim = simulate(EstMd1,K,'NumPaths',500,'Y0',serie_temporal,'E0',res);
%     yBar = mean(Ysim,2);
    
    % é o yF ou yBar que é o resultado da previsão? estou considerando que
    % é o yF. Se não for, mude esta parte final do código.
    previsoes(:,i) = yF;
end

save previsoes % salva um .mat
csvwrite('previsoes.csv', previsoes) % salva um CSV