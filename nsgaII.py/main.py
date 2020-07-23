import time

from pandas import DataFrame
import pandas as pd
import numpy as np
import nsga2

import matplotlib.pyplot as plt

# previsoes_acoes = pd.read_csv('previsoes.csv')

# valorizacao = previsoes_acoes.loc[363]/previsoes_acoes.loc[0]
# ler arquivo que possui dados das açoes
dados_acoes = pd.read_csv('otm2.csv')

# gerar mais dados de acordo com informações acima:
carteira = DataFrame(dados_acoes, columns=['preco_ativo', 'min_cotas', 'retorno_perc', 'risco_var'])

# filtra rendimentos percentuais menoras que 1
carteira = carteira[carteira.retorno_perc > 1]

# gerar estimativa de retorno absoluto
carteira['preco_minimo'] = carteira.preco_ativo * carteira.min_cotas
carteira['retorno_absoluto'] = carteira.preco_minimo * carteira.retorno_perc

# plot das acoes e seus riscos e retornos percentuais
plt.figure(1)
plt.xlabel('Retorno')
plt.ylabel('Risco')
plt.scatter(carteira.retorno_perc, carteira.risco_var)

population = 150
max_gen = 100
total_budget = 100000
num_execucoes = 15
generate_new = True

retorno = []
risco = []
solucoes = []
algorithm_start_time = time.time()
if generate_new:
    for i in range(0, num_execucoes):
        print("execução %s" % i)
        start_time = time.time()
        valores_retorno, valores_risco, solutions = nsga2.nsga2(population=population, carteira=carteira,
                                                                max_gen=max_gen, total_budget=total_budget)
        retorno = np.concatenate((retorno,  valores_retorno))
        risco = np.concatenate((risco,  valores_risco))
        solucoes.append(solutions)

        print("--- %s segundos ---" % (time.time() - start_time))


print("--- total: %s segundos ---" % (time.time() - algorithm_start_time))


    # salva variáveis
    # with open('conjunto_solucoes.pkl', 'w') as f:
    #     pickle.dump([retorno, risco, solucoes], f)

# else:
    # carrega arquivos (pra nao precisar rodar de novo)
    # with open('conjunto_solucoes.pkl', 'rb') as f:
    #     retorno, risco, solucoes = pickle.load(f)


# pega a fronteira pareto dentre as fronteiras pareto
non_dominated_sorted_solution = nsga2.non_dominated_sorting_algorithm(retorno[:], risco[:])


retorno_opt = retorno[non_dominated_sorted_solution[0]]
risco_opt = [-x for x in risco[non_dominated_sorted_solution[0]]]
# solucoes = solucoes[non_dominated_sorted_solution[0]]


# salva curva pareto em csv
fronteira_NSGAII = pd.DataFrame(data=[retorno_opt, risco_opt])
fronteira_NSGAII.to_csv('fronteira_NSGAII.csv')

# printa fronteiras
plt.figure()
for i in non_dominated_sorted_solution:
    plt.xlabel('Retorno')
    plt.ylabel('Risco')
    plt.scatter(retorno[i], [-x for x in risco[i]])
plt.show()

fig = plt.figure()
plt.xlabel('Retorno')
plt.ylabel('Risco')
plt.plot(retorno_opt, risco_opt, 'o')


# selecão de 4 soluções
# pontos = np.array([[122370, 0], [127898, 0], [130406, 0], [131500, 0]]) # TODO: pegar esses pontos por seleção na tela
#
#
# def distance(pt_1, pt_2):
#     return np.linalg.norm(pt_1-pt_2)
#
#
# def closest_node(node, nodes):
#     pt = []
#     dist = 9999999
#     for n in nodes:
#         if distance(node, n) <= dist:
#             dist = distance(node, n)
#             pt = n
#     return pt
#
#
# def closest_nodes(nodes_origin, nodes_compared):
#     pts = np.zeros([len(nodes_origin), 2])
#     i = 0
#     for n in nodes_origin:
#         pt = closest_node(n, nodes_compared)
#         pts[i][0] = pt[0]
#         pts[i][1] = pt[1]
#         i = i + 1
#     return pts
#
#
# solucoes = closest_nodes(pontos, np.array([retorno_opt[:], risco_opt[:]]).transpose())
# print(solucoes)
# [plt.plot(solucoes[i][0], solucoes[i][1], '*r') for i in range(0, len(solucoes))]
# plt.show()

# busca local nas 4 principais solucoes (gurobi para tudo? com epsilon restrito?)





