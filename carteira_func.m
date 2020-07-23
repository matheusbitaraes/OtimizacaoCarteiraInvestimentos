function [EstMdl,EstParamCov,logL,info] = carteira_func(serie_historica)

    dY = diff(serie_historica,2); % Diferenciando remove a tendencia linear dos dados, o que indica processo n�o-estacion�rio
    PC = parcorr(dY,25); % 25 valores de atraso para a funcao de autocorrelacao parcial
    
    AC = autocorr(dY,25); %25 valores de atraso para a funcao de autocorrelacao
    
    [ACF,lags,bounds] = autocorr(dY,[],2);

    lower_bound = min(bounds);

    indice_de_inicio = find(ACF<lower_bound);
    indice_de_inicio = indice_de_inicio(1);
    p = 0;
    for i = indice_de_inicio:length(ACF)
        if PC(i) >= lower_bound
            break;
        end
        p = p + 1;
    end
    
    [PACF,lags,bounds2] = parcorr(dY,[],2);

    lower_bound2 = min(bounds2);

    indice_de_inicio2 = find(PACF<lower_bound2);
    indice_de_inicio2 = indice_de_inicio2(1);
    q = 0;
    for i = indice_de_inicio2:length(PACF)
        if AC(i) >= lower_bound2
            break;
        end
        q = q + 1;
    end

    Md1 = arima(p,0,q);

    [EstMdl,EstParamCov,logL,info] = estimate(Md1,serie_historica);
end








