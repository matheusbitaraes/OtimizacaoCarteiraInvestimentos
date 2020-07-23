pkg load io
clear all
clc
disp("Importing data")
...xlsread("pareto_new");
...[numarr] = xlsread ("pareto_new")
load "otimizacao_carteira_investimentos.mat"
%load "optimization_data_eps_01.mat"
decision_variables = pareto_front
... N_matrix col = Custo de falha; custo de manutenção; Cfalha/cManutenção
c1 = 0.5;...peso do criterio 1 sobre menor risco
c2 = 0.5;... peso do criterio 2 sobre retorno
%c3 = 0.2;...peso do criterio 3 sobre relação retorno/risco
pesos = [c1,c2];
Concord_th = 0
Discord_th = 1
Concord_th = sort(pesos,2,"descend")(1,1);... + sort(pesos,2,"descend")(1,2);
Discord_th = min(pesos);
disp("Calculating normalized matrix")
for k = 1:1:length(decision_variables)
decision_variables(k,1) = decision_variables(k,2)/decision_variables(k,1);
%decision_variables(k,1) = 100 - decision_variables(k,1);
  endfor
for i = 1:1:length(decision_variables)
  for j=1:1:size(decision_variables,2)
  MaxValue = max(decision_variables);
  MinValue = min(decision_variables);
  N_Matrix(i,j) = pesos(1,j)*(decision_variables(i,j) - MinValue(1,j))/(MaxValue(1,j) - MinValue(1,j));
endfor
endfor
disp("Calculating Concordance and discordance Matrixes")
for i = 1:1:length(N_Matrix)
  for j = 1:1:length(N_Matrix)
    Concord_Matrix(j,i) = 0;
    for c=1:1:size(N_Matrix,2)
      if (N_Matrix(i,c) >= N_Matrix(j,c))
        Concord_Matrix(j,i) += pesos(1,c);
      else
        Concord_Matrix(j,i) += 0;
      endif
      if (N_Matrix(i,c) < N_Matrix(j,c))
        Discord_Matrix(j,i) = abs(min(N_Matrix(j,:) - N_Matrix(i,:)));
      else
        Discord_Matrix(j,i) = 0;
      endif
    endfor
  endfor
endfor

##for i = 1:1:length(N_Matrix)
##  for j = 1:1:length(N_Matrix)
##    Discord_Matrix(j,i) = 0;
##    for c=1:1:3
##      if (N_Matrix(i,c) > N_Matrix(j,c))
##        Discord_Matrix(j,i) = abs(min(N_Matrix(j,:) - N_Matrix(i,:)));
##      endif
##    endfor
##  endfor
##  i
##endfor
%Filtering
disp("Filtering")
for i = 1:1:length(N_Matrix)
  for j = 1:1:length(N_Matrix)
    Filtered_Matrix(j,i) = 0;   
    if (i != j)
      Filtered_Matrix(j,i) = 0;
      if (Concord_Matrix(j,i) >= Concord_th && Discord_Matrix(j,i) <= Discord_th)
        Filtered_Matrix(j,i) = 1;
      else
        Filtered_Matrix(j,i) = 0;
      endif
    else
      Filtered_Matrix(j,i) = 0;
    endif
  endfor
endfor
disp("Classificating")
%Classificação
for i=1:1:length(N_Matrix)
  Punctuation_Matrix(i,1) = i;
  Punctuation_Matrix(i,2) = sum(Filtered_Matrix(:,i));
endfor
[Classification_Matrix(:,2),Classification_Matrix(:,1)] = sort(Punctuation_Matrix(:,2),'descend');
Classification_Matrix
n=1;
while(n > 0)
n=0;
for i = 1:1:length(Punctuation_Matrix)
  for j = 1:1:length(Punctuation_Matrix)
    if (Punctuation_Matrix(i,2) == Punctuation_Matrix(j,2))
        Punctuation_Matrix(i,2) += Concord_Matrix(j,i);
        Punctuation_Matrix(i,2) -= Discord_Matrix(i,j);
        Punctuation_Matrix(j,2) += Concord_Matrix(i,j);
        Punctuation_Matrix(j,2) -= Discord_Matrix(j,i);
    endif
  endfor
endfor
endwhile
[Classification_Matrix(:,2),Classification_Matrix(:,1)] = sort(Punctuation_Matrix(:,2),'descend');
Classification_Matrix
%Saida
disp(strcat("A melhor escolha é o plano de manutenção de ID: ",num2str(Classification_Matrix(1,1))))
disp(strcat("Retorno: ",num2str(decision_variables(Classification_Matrix(1,1),2))))
disp(strcat("Risco: ",num2str(100-decision_variables(Classification_Matrix(1,1),1))))
save("Classificacao.mat", "Classification_Matrix","N_Matrix","decision_variables","Concord_th,Discord_th","c1","c2");
xlswrite("Classificacao.xlsx",Classification_Matrix);