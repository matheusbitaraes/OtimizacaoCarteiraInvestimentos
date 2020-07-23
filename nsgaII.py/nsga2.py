import math
import random
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame


def nsga2(population, carteira, total_budget, max_gen, show_plots=False):
    gen_no = 0
    solutions = solution_generator(population, ativos=carteira, total_budget=total_budget)
    # print(np.dot(solutions, carteira.preco_minimo) <= total_budget)
    # plt.figure()
    while (gen_no < max_gen):

        valores_retorno = [retorno(solutions[i], carteira) for i in range(0, population)]  # pega o retorno da solução
        valores_risco = [risco(solutions[i], carteira) for i in range(0, population)]  # pega o risco desta solucao

        # soluções não dominadas
        non_dominated_sorted_solution = non_dominated_sorting_algorithm(valores_retorno[:], valores_risco[:])

        # print('Generation:', gen_no, '\n')
        # for values in non_dominated_sorted_solution[0]:
        #     alocated = np.dot(solutions[values], carteira.preco_minimo)
        #     # if alocated > total_budget:
        #     #     print("eita")
        #     print('alocated:', alocated, '\n')
        #     print('remaining_budget:', total_budget - alocated, '\n')
        #     print(solutions[values], end=" ")
        # print("\n")

        # crowding distance
        crowding_distance_values = []
        for i in range(0, len(non_dominated_sorted_solution)):
            crowding_distance_values.append(
                crowding_distance(valores_retorno[:], valores_risco[:], non_dominated_sorted_solution[i][:]))
        solution2 = solutions[:]

        # cria novas soluções
        while len(solution2) != 2 * population:
            a1, b1 = random.sample(range(0, population - 1), 2)
            newsol = crossover(a=solutions[a1], b=solutions[b1], total_budget=total_budget, carteira=carteira)
            # print(np.dot(newsol, carteira.preco_minimo))
            solution2.append(newsol)

        # print(np.dot(solution2, carteira.preco_minimo) <= total_budget)
        # Calcula novos valores de retorno
        valores_retorno2 = [retorno(solution2[i], carteira) for i in range(0, 2 * population)]
        valores_risco2 = [risco(solution2[i], carteira) for i in range(0, 2 * population)]

        # novo calculo de soluções não dominadas
        non_dominated_sorted_solution2 = non_dominated_sorting_algorithm(valores_retorno2[:], valores_risco2[:])

        # novo crowding distance
        crowding_distance_values2 = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            crowding_distance_values2.append(
                crowding_distance(valores_retorno2[:], valores_risco2[:], non_dominated_sorted_solution2[i][:]))
        new_solution = []
        for i in range(0, len(non_dominated_sorted_solution2)):
            non_dominated_sorted_solution2_1 = [
                index_locator(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
                range(0, len(non_dominated_sorted_solution2[i]))]
            front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
            front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                     range(0, len(non_dominated_sorted_solution2[i]))]
            front.reverse()

            # selecão para proxima geração
            for value in front:
                new_solution.append(value)
                if len(new_solution) == population:
                    break
            if len(new_solution) == population:
                break
        solutions = [solution2[i] for i in new_solution]

        # print(np.dot(solutions, carteira.preco_minimo) <= total_budget)

        # plot
        if show_plots:
            plt.figure(2)
            plt.xlabel('Retorno')
            plt.ylabel('Risco')
            # plt.xlim((-100, 1000))
            # plt.ylim((-1000, 1000))
            plt.scatter([retorno(solutions[i], carteira) for i in non_dominated_sorted_solution[0]],
                        [-1 * risco(solutions[i], carteira) for i in non_dominated_sorted_solution[0]])
            # plt.scatter(valores_retorno2, valores_risco2, color='b')
            plt.draw()
            plt.pause(0.001)
        # plt.show(block=True)

        gen_no = gen_no + 1
    return valores_retorno, valores_risco, solutions


def retorno(x, carteira):
    # x = vetor de alocação de ativos
    return np.dot(x, carteira.retorno_absoluto)


def risco(x, carteira):
    return -1 * np.dot(x, carteira.risco_var)


def index_locator(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_locator(min(values), values) in list1:
            sorted_list.append(index_locator(min(values), values))
        values[index_locator(min(values), values)] = math.inf
    return sorted_list


def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 9999999999999999
    distance[len(front) - 1] = 9999999999999999
    for k in range(1, len(front)-1):
        distance[k] = distance[k] + (values1[sorted1[k+1]] - values2[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1, len(front)-1):
        distance[k] = distance[k] + (values1[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance


def mutation(x, carteira, total_budget):
    remaining_budget = total_budget - np.dot(x, carteira.preco_minimo)
    prob = random.random()
    if prob > 0.1:
        # a mutação remove alocacoes em uma posição e redistribui esse valor aleatoriamente
        sample_to_be_changed = x.sample()  # pega uma posição aleatoria
        removed_samples = np.round(random.random() * sample_to_be_changed)  # numero de cotas a serem removidas
        x[sample_to_be_changed.index] = x[sample_to_be_changed.index] - removed_samples
        remaining_budget = remaining_budget + carteira.preco_minimo[sample_to_be_changed.index] * removed_samples # recalcula o budget que está sobrando (levando em conta o budget que já estava sobrando)
        remaining_budget = remaining_budget.iloc[0]

        return alocate_remaining_budget(x, remaining_budget, carteira)
    return x


def crossover(a, b, total_budget, carteira):

    r = random.random()
    rand_index = random.sample(range(1, len(a) - 1), 1)
    perc_a = a/sum(a)
    perc_b = b/sum(b)
    if r > 0.5:
        child = np.hstack([perc_a[:rand_index[0]], perc_b[rand_index[0]:]])
        # child[rand_index[0]:len(child)] = b[rand_index[0]:len(b)]   #ESTÁ COM ERRO NESSA PARTE
    else:
        # child = perc_b
        # child[rand_index[0]:len(child)] = a[rand_index[0]:len(a)]
        child = np.hstack([perc_a[:rand_index[0]], perc_b[rand_index[0]:]])

    # child_val = child * carteira.preco_minimo
    if sum(child) > 0:
        child_perc = child/sum(child)  # percentual do novo filho
    else:
        child_perc = perc_a

    # pega porcentagem do valor total a ser dividido e aloca de acordo com as cotas minimas
    x = np.floor((total_budget * child_perc) / carteira.preco_minimo)
    alocated_budget = sum(x * carteira.preco_minimo)

    child = alocate_remaining_budget(alocation=x, remaining_budget=total_budget - alocated_budget, ativos=carteira)
    return mutation(x=child, carteira=carteira, total_budget=total_budget)


def non_dominated_sorting_algorithm(values1, values2):
    S = [[] for i in range(0, len(values1))]
    front = [[]]
    n = [0 for i in range(0, len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while front[i] != []:
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if n[q]==0:
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front)-1]
    return front


def alocate_remaining_budget(alocation, remaining_budget, ativos):
    while (True):
        # pega aleatoriamente uma ação de maior valor minimo que o budget restante pode pagar
        available_assets = ativos[ativos.preco_minimo <= remaining_budget]
        if len(available_assets) == 0:
            break
        asset = available_assets.sample()  # pega aleatoriamente uma das açoes disponiveis
        alocation_multiplier = np.floor(remaining_budget / asset.preco_minimo)
        alocation_value = alocation_multiplier * asset.preco_minimo
        alocation[asset.index] = alocation[asset.index] + alocation_multiplier
        remaining_budget = remaining_budget - alocation_value.iloc[0]
    return alocation


def solution_generator(population_size, ativos, total_budget):
    solutions = []
    for i in range(0, population_size):
        # gera porcentagens aleatórias iniciais estimadas para a alocação dos ativos
        randsol = 10 * np.random.rand(len(ativos.preco_ativo), )
        raw_alocation = randsol / randsol.sum(0)

        # pega porcentagem do valor total a ser dividido e aloca de acordo com as cotas minimas
        x = np.floor((total_budget * raw_alocation) / ativos.preco_minimo)
        alocated_budget = sum(x * ativos.preco_minimo)

        # agora vamos alocar o restante "quebrado" que não pode ser alocado, devido a limitacao de cotas
        remaining_budget = total_budget - alocated_budget

        while (True):  # TODO: substituir pela função alocate_remaining_budget
            # pega aleatoriamente uma ação de maior valor minimo que o budget restante pode pagar
            available_assets = ativos[ativos['preco_minimo'] <= remaining_budget]
            if len(available_assets) == 0:
                break
            asset = available_assets.sample()  # pega aleatoriamente uma das açoes disponiveis
            alocation_multiplier = np.floor(remaining_budget / asset.preco_minimo)
            alocation_value = alocation_multiplier * asset.preco_minimo
            x[asset.index] = x[asset.index] + alocation_multiplier
            remaining_budget = remaining_budget - alocation_value.iloc[0]

        solutions.append(x)

    return solutions


def non_dominating_curve_plotter(valores_retorno, valores_risco):   # plot
    plt.figure(3)
    plt.xlabel('Retorno')
    plt.ylabel('Risco')
    # risco = [-x for x in valores_risco]
    plt.scatter(valores_retorno, [-x for x in valores_risco])
    # plt.show()
