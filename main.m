% leitura dos arquivos
clc
clear model

total_budget = 100000;
dados_acoes = csvread('otm_matlab.csv'); % [ID, t0, cluster, custo falha]
preco_ativo = dados_acoes(:,1);
min_cotas = dados_acoes(:,2);
retorno_perc = dados_acoes(:,3);
risco_var = dados_acoes(:,4);
preco_minimo = preco_ativo.*min_cotas;
retorno_absoluto = preco_minimo.*retorno_perc;

numero_acoes = size(dados_acoes,1);

% Initialize model
model.modelsense  = 'max';
model.modelname   = 'multiobj';

% Set variables and constraints
model.vtype       = repmat('i', numero_acoes,1);
model.lb          = zeros(numero_acoes, 1);
model.A           = sparse([risco_var' ; preco_minimo']);
model.sense       = '<';
model.obj     = retorno_absoluto;

step = 1; % variacao do epsilon

% vetor de progressao do epsilon
vetor_epsilon = [(0.01:0.1:10) (11:1:100)];

% carrega fronteira gerada pelo modelo genético
nsga_front = csvread('./nsgaII.py/fronteira_NSGAII.csv');
nsga_risco = nsga_front(3,2:end)';
nsga_retorno = nsga_front(2,2:end)';

figure()
title('Fronteira pareto')
ylabel('Risco')
xlabel('Retorno')
hold on

plot(nsga_retorno,nsga_risco, '*r') %plota resultados do nsgaII

i = 1;
pareto_front = [];
optimal_x = [];
tic
for epsilon = 1:length(vetor_epsilon)
    
    model.rhs = [vetor_epsilon(epsilon); total_budget+1]; % atualiza epsilon
    % Otimiza
    result = gurobi(model);

    % verifica solução
    if strcmp(result.status, 'OPTIMAL')
        risco_total = sum(result.x .* risco_var);
        plot(result.objval, risco_total, '*b')
        pareto_front(i,1) = risco_total;
        pareto_front(i,2) = result.objval;
        optimal_x(i,:) = result.x .* preco_minimo;
        i = i + 1;
    end
end
toc

% armazena resultados
% decision_variables(:,1:2) = pareto_front;
unique_values = unique([pareto_front optimal_x], 'rows');
pareto_front = unique_values(:,1:2);
optimal_x = unique_values(:,3:end);

save ('otimizacao_carteira_investimentos',...
    'pareto_front','optimal_x', 'decision_variables')

% exporta para csv
csvwrite('resultadosCarteiraInvestimentos.csv', optimal_x)

% execução 0
% --- 282.12830114364624 segundos ---
% execução 1
% --- 261.8729200363159 segundos ---
% execução 2
% --- 265.38857316970825 segundos ---
% execução 3
% --- 259.71364307403564 segundos ---
% execução 4
% --- 268.59018874168396 segundos ---
% execução 5
% --- 261.2554507255554 segundos ---
% execução 6
% --- 254.25737404823303 segundos ---
% execução 7
% --- 259.23268008232117 segundos ---
% execução 8
% --- 256.5040702819824 segundos ---
% execução 9
% --- 258.6489200592041 segundos ---
% execução 10
% --- 256.32034492492676 segundos ---
% execução 11
% --- 250.93598699569702 segundos ---
% execução 12
% --- 256.2195429801941 segundos ---
% execução 13
% --- 264.7919888496399 segundos ---
% execução 14
% --- 263.7117819786072 segundos ---
% --- total: 3919.572249889374 segundos ---