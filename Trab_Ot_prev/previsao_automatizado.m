% leitura do arquivo de dados
ativos_series_temporais = csvread('c:\Trab_Ot_prev\ativos_series_temporais.csv',1,0);
K = 365; % dias
previsoes = zeros(K, size(ativos_series_temporais, 2));

for i = 1 : size(ativos_series_temporais, 2)
    serie_temporal = ativos_series_temporais(:, i);
    
    % retira zeros do final
    serie_temporal = serie_temporal(find(serie_temporal>0));
    
    % gera valores da serie temporal
    try
        [EstMdl,EstParamCov,logL,info] = carteira_func(serie_temporal);

        [yF,yMSE] = forecast(EstMdl,K,'Y0',serie_temporal);

        rng 'default';
        res = infer(EstMdl,serie_temporal);
    %     Ysim = simulate(EstMd1,K,'NumPaths',500,'Y0',serie_temporal,'E0',res);
        Ysim = simulate(EstMdl,K,'Y0',serie_temporal,'E0',res);
    %     yBar = mean(Ysim,2);

        % é o yF ou yBar que é o resultado da previsão? estou considerando que
        % é o yF. Se não for, mude esta parte final do código.
        previsoes(:,i) = yF;

        %% plot (comentar para melhor performance)
    %     T = length(serie_temporal);
    %     upper = yF + 1.96*sqrt(yMSE);
    %     lower = yF - 1.96*sqrt(yMSE);
    %     
    %     figure
    %     plot(serie_temporal,'Color',[.75,.75,.75])
    %     hold on
    %     plot(T+1:T+K,Ysim,'-r')
    %     h1 = plot(T+1:T+K,yF,'r', 'LineWidth',2);
    %     h2 = plot(T+1:T+K,upper, 'k--', 'Linewidth', 1.5);
    %     plot(T+1:T+K,lower, 'k--', 'LineWidth', 1.5)
    %     xlim([0,T+K])
    %     title('Previs�o e Intervalo de Previs�o de 95%')
    %     hold off

        save previsoes % salva um .mat
    catch ERRO
        warning (['erro na acao' i])
    end
end

save previsoes % salva um .mat
csvwrite('previsoes.csv', previsoes) % salva um CSV