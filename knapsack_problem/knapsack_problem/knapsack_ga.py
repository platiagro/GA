#knapsack_ga.py
#Author: Oclair Prado em mar/2020

from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
import time


class Candidate:
    np_dna = np.array([])
    weight = 0
    benefit = 0  

    def get_weight(self): 
        return self.weight

    def get_benefit(self): 
        return self.benefit

    def fitness_evaluation(self, prod_list):
        if prod_list == None:
            raise ValueError

        self.weight = np.sum(self.np_dna * prod_list.np_weight_list)
        self.benefit = np.sum(self.np_dna * prod_list.np_benefit_list)        

    def __init__(self, prod_list):
        dna = []
        tot = len(prod_list.np_weight_list)
        
        for pos in range(0, tot):
            dna.append(randint(0, 1))

        np_dna_new = np.array(dna)
        self.np_dna = np_dna_new
        self.fitness_evaluation(prod_list)

    

class ObjectsList:
    np_weight_list = np.array([])
    np_benefit_list = np.array([])

    def __init__(self, qtd_obj):
        if qtd_obj == None:
            raise ValueError

        weight_list = []
        benefit_list = []

        for pos in range(0, qtd_obj):
            weight_list.append(randint(100, 2000))
            benefit_list.append(randint(1, 10))
        
        self.np_weight_list = np.array(weight_list)
        self.np_benefit_list = np.array(benefit_list)    



def stop_search(weight_limit, weight_tolerance, population, best_fit_array, medium_fit_array, generation, obj_list):
    if weight_limit <= 0:
        raise ValueError
    if weight_tolerance <= 0:
        raise ValueError
    if population == None:
        raise ValueError
    if best_fit_array == None:
        raise ValueError
    if medium_fit_array == None:
        raise ValueError
    if generation <= 0:
        raise ValueError
    if obj_list == None:
        raise ValueError

    ret = False

    best_benefit = 0
    best_weight = 0

    medium_benefit = 0
    medium_weight = 0

    benefit_amount = 0
    wigth_amount = 0

    #Calcula fitness medio da populacao e guarda o fitness do melhor candidato
    for cand in population:
        benefit_amount += cand.benefit
        wigth_amount += cand.weight
        #Precisa pular a primeira geracao porque ainda nao foi filtrada
        if generation < 1:
            generation_new = 1
        else:    
            if cand.benefit > best_benefit:
                best_candidate = cand

                best_benefit = cand.benefit
                best_weight = cand.weight
            
                adjusted_weight_limit = weight_limit * 1000 #Ajustado para gramas
                if best_weight <= adjusted_weight_limit and adjusted_weight_limit - best_weight < weight_tolerance:
                    ret = True
                    #Mostra dados do melhor candidato
                    print("weight: {0}, benefit: {1}, DNA: {2}".format(best_candidate.weight, best_candidate.benefit, best_candidate.np_dna))
    
                    print( "Weight : {0}".format( obj_list.np_weight_list ))
                    print( "Benetif: {0}".format( obj_list.np_benefit_list ))

    if generation > 30 and best_benefit == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_benefit = best_fit_array[generation - 1]

    medium_benefit = benefit_amount / len(population)
    medium_weight = wigth_amount / len(population)

    #Registra resultados    
    best_fit_array.append(best_benefit)
    medium_fit_array.append(medium_benefit)

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 30:
        adjusted_weight_limit = weight_limit * 1000 #Ajustado para gramas
        if(best_weight <= adjusted_weight_limit and
           best_fit_array[generation - 1] == best_fit_array[generation - 2] and
           best_fit_array[generation - 2] == best_fit_array[generation - 3] and
           best_fit_array[generation - 3] == best_fit_array[generation - 4] ):
           ret = True
           #Mostra dados do melhor candidato
           print("weight: {0}, benefit: {1}, DNA: {2}".format(best_candidate.weight, best_candidate.benefit, best_candidate.np_dna))
    
           print( "Weight : {0}".format( obj_list.np_weight_list ))
           print( "Benetif: {0}".format( obj_list.np_benefit_list ))

    #Mostra resultados
    print("Generation: {0} - best benefit / weight: {1} / {2} - medium benefit / weight: {3} / {4}".format(generation, best_benefit, best_weight, medium_benefit, medium_weight))
    
    return ret



def search(weight_tolerance = 100):
    if weight_tolerance <= 0:
        raise ValueError

    ini_pop_qt = 200  #Usar 1000
    intermed_pop_qt = 2000 #usar 10000
    #mutation_rate = 0.8  #Testando com 20%
    crossover_rate = 0.2 #Testando com 80%

    exec_init = time.time()

    print("\n##################################################################")
    print("#                                                                #")
    print("#                     Knapsack problem                           #")
    print("#                                                                #")
    print("##################################################################")

    try:
        weight_limit = int(float(input("\nKnapsack weight limit: ")))
        if weight_limit <= 0:
            print("\nKnapsack weight limit must be higher than zero!\n")
            raise ValueError
    except:
        raise ValueError

    try:
        available_objects_qt = int(float(input("\nAvailable objects (limit: 1010): ")))
        if available_objects_qt <= 0:
            print("\nAvailable objects must be higher than zero!\n")
            raise ValueError

        else:    
            if available_objects_qt > 1010:
                print("Values higher than 1010 are forbiden!")
                raise ValueError

            elif available_objects_qt <= 15:
                print("There are " + str(2 ** available_objects_qt) + " possible solutions for this products amount")
            else:
                possible_solutions = 2 ** available_objects_qt
                search_years = possible_solutions / (3600 * 24 * 365 * 1000000)
                print("There are {0:+5.2E} possible solutions for this products amount".format(possible_solutions))
                if available_objects_qt > 44:
                    print("\nIf we had a computer capable of processing 1.000.000 candidates each second")
                    print("and considering that one year has (60s * 60m * 24h * 365d) 31.536.000 seconds")
                    print("it would take {0:+5.2e} years to find the best solution.".format(search_years))
                    print("Therefore, we'll search for just a good solution, not for the best one.")
                    print("The good solution will be the candidate with the best benefit within the limit of weight\n")
    except:
        raise ValueError

    obj_list = ObjectsList(available_objects_qt)
    populat = create_initial_population(ini_pop_qt, obj_list)
    population = sorted(populat, key = Candidate.get_benefit, reverse = True)

#    print("Mostra a populacao inicial: ")
#    for pos in range(0, len(population)):
#        print("weight: {0}, benefit: {1}, DNA: {2}".format(population[pos].weight, population[pos].benefit, population[pos].np_dna))
    
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    #Repete este ciclo ate condicao de parada
    while not stop_search(weight_limit, weight_tolerance, population, best_fit_array, medium_fit_array, generation, obj_list):
        #Cria nova população intermediaria com mutacao e crossover
        #Para manter a diversidade genetica a semente para a proxima geracao sera formada por 40% dos melhores candidatos atuais e 10% dos piores
        
        #==>Seleciona os pais para reproducao
        best_cand_qt = int(40 * ini_pop_qt / 100)
        worst_cand_qt = int(10 * ini_pop_qt / 100)
        cand_for_reproduction_1 = np.copy(population[:best_cand_qt])
        cand_for_reproduction_2 = np.copy(population[ini_pop_qt - worst_cand_qt:])
        cand_for_reproduction = np.append(cand_for_reproduction_1, cand_for_reproduction_2)
        
        #==>Reproducao por CROSSOVER
        crossover_qt = int(crossover_rate * (intermed_pop_qt - len(cand_for_reproduction)))
        if (crossover_qt % 2) != 0:
            crossover_qt = crossover_qt + 1

        intermed_pop_crossover = apply_crossover(crossover_qt, cand_for_reproduction, obj_list)
    
        #==>Reproducao por MUTAÇÃO
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>Selecao da proxima geracao de candidatos
        intermed_pop_mutation = apply_mutation(mutation_qt, cand_for_reproduction, obj_list)
    
        intermed_pop_mutation = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop_mutation = np.append(intermed_pop_mutation, intermed_pop_mutation)
        print("Size of intermed pop: {0}".format(len(intermed_pop_mutation)))

        population = apply_selection(ini_pop_qt, weight_limit, intermed_pop_mutation)

        #Registra parte dos resultados
        generation = generation + 1
        xItera.append(generation)

    #Mostra tempo de execucao
    exec_end = time.time()
    diff = exec_end - exec_init	
    hours, r = divmod(diff, 3600)
    minutes, seconds = divmod(r, 60)
    print("Elapsed time: {hours:0>2}:{minutes:0>2}:{seconds:05.3f}".format(hours=int(hours), minutes=int(minutes), seconds=seconds))

    #Mostra evolucao do fitness
    plt.rcParams['figure.figsize'] = (8,4)
    plt.plot(xItera, medium_fit_array, color='green')  #Fitness medio
    plt.scatter(xItera, best_fit_array, marker="*", color='red') #Melhor fitness
    plt.title('Benefit (fitness) evolution')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (benefit)')
    plt.grid(True)
    plt.show()
    return "ok"



def apply_selection(qtd_pop, weight_limit, pop_inter):
    if qtd_pop <= 0:
        raise ValueError
    if weight_limit <= 0:
        raise ValueError
    if pop_inter == None:
        raise ValueError
    
    #Fase 1: elimina candidatos acima do peso ate limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o peso
    #Remove todos acima do pelo limite ou ate sobre somente qtd_pop
    
    #Fase 2: elimina candidatos com menor beneficio ate o limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o beneficio
    #Enquanto tamanho da populacao nao baixar para o tamanho desejado

    #Fase 1
    pop_sorted_by_weight = sorted( pop_inter, key = Candidate.get_weight, reverse = True)
    dismissed = True
    cand = pop_sorted_by_weight[0]
    if cand.weight > (weight_limit * 1000): #Peso do candidatos em gramas
        dismissed = True
    else:
        dismissed = False

    while len(pop_sorted_by_weight) > qtd_pop and dismissed == True:
        pop_sorted_by_weight = np.delete(pop_sorted_by_weight, 0)
        cand = pop_sorted_by_weight[0]
        if cand.weight > (weight_limit * 1000):
            dismissed = True
        else:
            dismissed = False

    #Fase 2
    pop_sorted_by_benefit = sorted( pop_sorted_by_weight, key = Candidate.get_benefit, reverse = True)
 
    pop_sorted_by_benefit = pop_sorted_by_benefit[0:qtd_pop]
    
    return pop_sorted_by_benefit



def apply_crossover(crossover_qt, cand_to_repro, obj_list):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro == None:
        raise ValueError
    if obj_list == None:
        raise ValueError

    #A qtd_crossover indica a quantidade de descendentes a ser produzida
    #Em cada ciclo sao criados dois novos descendentes
    #Entao serao realizados "qtd_crossover/2" ciclos
    #Em cada ciclo:
        #Seleciona 2 pais da lista de candidatos a reproducao, p1 e p2
        #Seleciona ponto de crossover
        #Cria dois novos candidatos, f1 e f2
        #Copia DNA de p1 até o ponto de crossover para o inicio de f1
        #Copia DNA de p1 após o ponto de crossover para o fim de f2
        #Copia DNA de p2 até o ponto de crossover para o inicio de f2
        #Copia DNA de p2 após o ponto de crossover para o fim de f1
        #Acrescenta novos filhos na lista parcial de candidatos
    #Devolve a lista parcial criada
    
    new_pop_crossover = []
    np_new_pop_crossover = np.array(new_pop_crossover)

    qtd_cicles = int(crossover_qt / 2)
    for pos in range(0, qtd_cicles):
        choice_limit = len(cand_to_repro) - 2
        cand_position1 = randint(1, choice_limit)
        p1 = cand_to_repro[cand_position1] #Seleciona p1
        #Obs.: p2 deve ser diferente de p1 para evitar perda de diversidade genetica
        cand_position2 = randint(1, choice_limit)
        while cand_position1 == cand_position2: 
           cand_position2 = randint(1, choice_limit)
        p2 = cand_to_repro[cand_position2] #Seleciona p2

#        #Mostra DNA dos pais
#        print("[Father 1]weight: {0} Benef: {1} DNA: {2}".format(p1.weight, p1.benefit, p1.np_dna))
#        print("[Father 2]weight: {0} Benef: {1} DNA: {2}".format(p2.weight, p2.benefit, p2.np_dna))

        dna_length = len(p1.np_dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Candidate(obj_list) #DNA ja foi criado mas sera alterado por crossover
        f2 = Candidate(obj_list) #DNA tambem sera alterado
        
        #Copia parte de p1 para f1 e parte de f2 para p2
        for pos in range(0, pto_cross): #Adorei esse foreach() esquisitao
            f1.np_dna[pos] = p1.np_dna[pos]
            f2.np_dna[pos] = p2.np_dna[pos]

        #Copia parte de p1 para f2 e parte de p2 para f1    
        for pos in range(pto_cross, dna_length):
            f1.np_dna[pos] = p2.np_dna[pos]
            f2.np_dna[pos] = p1.np_dna[pos]

        #Ajusta fitness dos novos candidatos
        f1.fitness_evaluation(obj_list)
        f2.fitness_evaluation(obj_list)   

        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)

#        #Mostra DNA dos filhos
#        print("Crossover point: " + str(pto_cross))
#        print("[Filho 1]weight: {0} Benef: {1} DNA: {2}".format(f1.weight, f1.benefit, f1.np_dna))
#        print("[Filho 2]weight: {0} Benef: {1} DNA: {2}".format(f2.weight, f2.benefit, f2.np_dna))

    return np_new_pop_crossover


def apply_mutation(wished_qt, cand_to_repro, obj_list):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro == None:
        raise ValueError
    if obj_list == None:
        raise ValueError

    #Cada candidato tem seu vetor de zeros e uns (DNA[])
    #Cada candidato selecionado gera um clone
    #Aplica mutacao no novo candidato
    
    new_pop_mutation = []
    np_new_pop_mutation = np.array(new_pop_mutation)

    for pos in range(0, wished_qt):
        #Seleciona aleatoriamente um membro do grupo de candidatos a reproducao
        new_cand = Candidate(obj_list)  #Este novo candidato vai receber o DNA alterado por mutacao
        choice_limit = len(cand_to_repro) - 1
        cand_position = randint(0, choice_limit)
        cand = cand_to_repro[cand_position]
        new_cand.np_dna = np.copy(cand.np_dna)

        #Aplica mutacao em um ponto de seu DNA
        mutation_limit = len(new_cand.np_dna) - 1
        mutation_target = randint(0, mutation_limit)
        if new_cand.np_dna[mutation_target] == 0:                                                                                                                
            new_cand.np_dna[mutation_target] = 1
        else:
            new_cand.np_dna[mutation_target] = 0
        
        new_cand.fitness_evaluation(obj_list)

#        #Mostra DNA do pai
#        print("[Father]weight: {0} Benef: {1} DNA: {2}".format(cand.weight, cand.benefit, cand.np_dna))
#        #Mostra DNA dos pais
#        print("[Son]weight: {0} Benef: {1} DNA: {2}".format(new_cand.weight, new_cand.benefit, new_cand.np_dna))
    
        #Insere novo candidato na populacao intermediaria
        np_new_pop_mutation = np.append(np_new_pop_mutation, new_cand)
        
    return np_new_pop_mutation
    

def create_initial_population(init_pop_qt, obj_list):
    if init_pop_qt <= 0:
        raise ValueError
    if obj_list == None:
        raise ValueError
    
    pop = []
    for pos in range(0, init_pop_qt):
        cand = Candidate(obj_list)
        pop.append(cand)
    return pop
    


if __name__ == '__main__':
#    weight_tolerance = 100 #100 gramas

#    search(weight_tolerance)
    search()
    
