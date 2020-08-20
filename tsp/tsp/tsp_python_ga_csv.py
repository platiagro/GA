#knapsack_ga.py
#Author: Oclair Prado em ago/2020

import random
from random import uniform, randint
import numpy as np
import pandas as pd
import time


class Candidate:
    dna = []
    fitness = 0

    def get_fitness(self):
        return self.fitness

    def fitness_evaluation(self, resources):
        if resources is None:
            raise ValueError

        dict_dist = resources.dict_dist
        tot_dist = 0
        for id in range(1,len(self.dna)):
            city_x = self.dna[id]
            city_y = self.dna[id-1]
            try:
                dist = dict_dist[city_x][city_y]
            except:
                dist = dict_dist[city_y][city_x]
            tot_dist += dist
        self.fitness = 1/tot_dist


    def generate_dna(self, resources):
        if resources is None:
            raise ValueError

        dna = []
        cities = resources.cities
        tot = len(cities)
        dict_dist = resources.dict_dist

        options = [k for k in cities]
        while len(dna) < len(cities):
            new_city = random.choice(options)
            ind = options.index(new_city)
            dna.append(new_city)
            del options[ind]
        self.dna = dna


    def __init__( self, resources ):
        if resources is None:
            raise ValueError
        
        self.dna = []
        self.generate_dna( resources )



class Resources:
    dict_dist = {}
    cities = []
    best_candidate = None


    def set_best_candidate( self, best ):
        if best is None:
            raise ValueError
        self.best_candidate = best


    def get_best_candidate( self ):
        return self.best_candidate


    def get_selected_route( self ):
        response = {}
        #| Orig | Dest | Dist |
        acum_dist = 0

        column_orig_name = "Origem"
        column_orig = []
        column_dest_name = "Destino"
        column_dest = []
        column_km_name = "KM"
        column_km = []
        
        qtd = len(self.best_candidate.dna) - 1
        for pos in range( 0, qtd ):
            city_x = self.best_candidate.dna[pos]
            city_y = self.best_candidate.dna[pos + 1]
            try:
                dist = self.dict_dist[city_x][city_y]
            except:
                dist = self.dict_dist[city_y][city_x]

            column_orig.append( city_x )
            column_dest.append( city_y )
            column_km.append( dist )

            acum_dist += dist
                    
        column_orig.append( "Total" )
        column_dest.append( "" )
        column_km.append( acum_dist )
        
        response[column_orig_name] = column_orig
        response[column_dest_name] = column_dest
        response[column_km_name] = column_km
                        
        pd_response = pd.DataFrame( data = response )
        return pd_response


    def __init__(self, pd_resources):
        if pd_resources is None:
            raise ValueError

        cities = []
        for ind in pd_resources.itertuples():
            if ind[1][0:1].lower() != "origem":
                #   0     1     2 
                #  Origem, Destino, Dist
                cities.append(ind[1])
                cities.append(ind[2])
        cities = sorted(set(cities))
        self.cities = cities

        dict_dist = {}
        dict_dist = {cit:{} for cit in cities}

        for ind in pd_resources.itertuples():
            if ind[1][0:1].lower() != "origem":
                #   0     1     2 
                #  Origem, Destino, Dist
                city_x = ind[1]
                city_y = ind[2]
                dict_dist[city_x][city_y] = ind[3]

        self.dict_dist = dict_dist
        #print( dict_dist )





def search( resources ):
    if resources is None:
        raise ValueError

    ini_pop_qt = 200  
    intermed_pop_qt = 2000 
    #mutation_rate = 0.8  #Testando com 20%
    crossover_rate = 0.2 #Testando com 80%

    populat = create_initial_population(ini_pop_qt, resources)
    population = sorted(populat, key = Candidate.get_fitness, reverse = True)
 
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    #Repete este ciclo ate condicao de parada
    while not stop_search( population, best_fit_array, medium_fit_array, generation, resources ):
        #Cria nova populacao intermediaria com mutacao e crossover
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

        intermed_pop_crossover = apply_crossover(crossover_qt, cand_for_reproduction, resources )
    
        #==>Reproducao por MUTACAO
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>Selecao da proxima geracao de candidatos
        intermed_pop_mutation = apply_mutation(mutation_qt, cand_for_reproduction, resources)
    
        intermed_pop_mutation = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop_mutation = np.append(intermed_pop_mutation, intermed_pop_mutation)
#        print("Size of intermed pop: {0}".format(len(intermed_pop_mutation)))

        population = apply_selection(ini_pop_qt, intermed_pop_mutation)

        #Registra parte dos resultados
        generation = generation + 1
        xItera.append(generation)

    return "ok"



def stop_search( population, best_fit_array, medium_fit_array, generation, resources ):
    if population is None:
        raise ValueError
    if best_fit_array is None:
        raise ValueError
    if medium_fit_array is None:
        raise ValueError
    if generation <= 0:
        raise ValueError
    if generation is None:
        raise ValueError
    if resources is None:
        raise ValueError

    ret = False

    best_fitness = 0
    medium_fitness = 0
    fitness_amount = 0

    #Calcula fitness medio da populacao e guarda o fitness do melhor candidato
    for cand in population:
        fitness_amount += cand.fitness
        #Precisa pular a primeira geracao porque ainda nao foi filtrada
        if generation > 1:
            fitness_amount += cand.fitness
            if cand.fitness > best_fitness:
                best_candidate = cand
                best_fitness = cand.fitness
                
    if generation > 1 and best_fitness == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_fitness = best_fit_array[generation - 1]

    medium_fitness = fitness_amount / len(population)

    #Registra resultados    
    best_fit_array.append(best_fitness)
    medium_fit_array.append(medium_fitness)

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 30:
        if(best_fit_array[generation - 1] == best_fit_array[generation - 2] and
           best_fit_array[generation - 2] == best_fit_array[generation - 3] and
           best_fit_array[generation - 3] == best_fit_array[generation - 4] ):
           ret = True
           resources.set_best_candidate( best_candidate )
           #Mostra dados do melhor candidato
           print("Best fitness: {0}, DNA: {1}".format(best_candidate.fitness, best_candidate.dna))    
           print( "Distance : {0}".format( int(1/best_candidate.fitness) ))

    #Mostra resultados
    if (generation % 5) == 0:
        print("Generation: {0} - best fitness [{1}] - medium fitness [{2}] - distance [{3}]".format(generation, best_fitness, medium_fitness, int(1/best_fitness)))

    return ret



def apply_selection(qtd_pop, pop_inter):
    if qtd_pop <= 0:
        raise ValueError
    if pop_inter is None:
        raise ValueError

    pop_sorted_by_fitness = sorted( pop_inter, key = Candidate.get_fitness, reverse = True)
    pop_sorted = pop_sorted_by_fitness[0:qtd_pop]
    
    return pop_sorted



def apply_mutation(wished_qt, cand_to_repro, resources):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError

    #seleciona 2 posicoes e troca uma com a outra
    new_pop_mutation = []
    np_new_pop_mutation = np.array(new_pop_mutation)

    for pos in range(0, wished_qt):
        #Seleciona aleatoriamente um membro do grupo de candidatos a reproducao
        new_cand = Candidate(resources)  #Este novo candidato vai receber o DNA alterado por mutacao
        choice_limit = len(cand_to_repro) - 1
        cand_position = randint(0, choice_limit)
        cand = cand_to_repro[cand_position]
        new_cand.dna = np.copy(cand.dna)

        #Aplica mutacao em dois pontos diferentes de seu DNA
        mutation_limit = len(new_cand.dna) - 1
        mutation_target1 = randint(0, mutation_limit)
        mutation_target2 = randint(0, mutation_limit)
        while mutation_target2 == mutation_target1:
            mutation_target2 = randint(0, mutation_limit)

        tmp_city = new_cand.dna[mutation_target1]                                                                                                                
        new_cand.dna[mutation_target1] = new_cand.dna[mutation_target2]
        new_cand.dna[mutation_target2] = tmp_city
        
        new_cand.fitness_evaluation(resources)
    
        #Insere novo candidato na populacao intermediaria
        np_new_pop_mutation = np.append(np_new_pop_mutation, new_cand)
        
    return np_new_pop_mutation
    

def apply_crossover(crossover_qt, cand_to_repro, resources):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError

    #A qtd_crossover indica a quantidade de descendentes a ser produzida
    #Em cada ciclo sao criados quatro novos descendentes
    #Entao serao realizados "qtd_crossover/4" ciclos
    #Em cada ciclo:
        #Seleciona 2 pais da lista de candidatos a reproducao, p1 e p2
        #Seleciona ponto de crossover
        #Cria quatro novos candidatos, f1, f2, f3 e f4
        #Copia os índices de P1 até Px para o filho f1 e o restante de f1 é completado aleatoriamente para evitar corromper o candidato
        #Copia os índices de P1 após Px para o filho f2 e o restante é completado aleatoriamente 
        #Copia os índices de P2 até Px para f3 e o restante é completado aleatoriamente
        #Copia os índices de p2 após Px para f4 e o restante é completado aleatoriamente
        #Acrescenta novos filhos na lista parcial de candidatos
    #Devolve a lista parcial criada
    
    new_pop_crossover = []
    np_new_pop_crossover = np.array(new_pop_crossover)

    qtd_cicles = int(crossover_qt / 4)
    for pos in range(0, qtd_cicles):
        choice_limit = len(cand_to_repro) - 2
        cand_position1 = randint(1, choice_limit)
        p1 = cand_to_repro[cand_position1] #Seleciona p1
        
        cand_position2 = randint(1, choice_limit)
        while cand_position1 == cand_position2: #Obs.: p2 deve ser diferente de p1 para evitar perda de diversidade genetica
           cand_position2 = randint(1, choice_limit)
        p2 = cand_to_repro[cand_position2] #Seleciona p2

        dna_length = len(p1.dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Candidate(resources) #DNA ja foi criado mas sera alterado por crossover
        f2 = Candidate(resources) #DNA tambem sera alterado
        f3 = Candidate(resources)
        f4 = Candidate(resources)

        #F1
        #Copia os índices de P1 até Px para o filho f1 e o restante de f1 é completado aleatoriamente para evitar corromper o candidato
        cities = resources.cities
        dict_dist = resources.dict_dist
        options = [k for k in cities]
        
        for pos in range(0, pto_cross): #Copy
            f1.dna[pos] = p1.dna[pos]
            ind = options.index(p1.dna[pos])
            del options[ind]
        
        for pos in range(pto_cross, dna_length): #Random
            new_city = random.choice(options)
            f1.dna[pos] = new_city
            ind = options.index(new_city)
            del options[ind]
        
        #F2
        #Copia os índices de P1 após Px para o filho f2 e o restante é completado aleatoriamente 
        options = [k for k in cities]

        for pos in range(pto_cross, dna_length): #Copy
            f2.dna[pos] = p1.dna[pos]
            ind = options.index(p1.dna[pos])
            del options[ind]

        for pos in range(0, pto_cross): #Random
            new_city = random.choice(options)
            f2.dna[pos] = new_city
            ind = options.index(new_city)
            del options[ind]    

        #F3                
        #Copia os índices de P2 até Px para f3 e o restante é completado aleatoriamente
        options = [k for k in cities]

        for pos in range(0, pto_cross): #Copy
            f3.dna[pos] = p2.dna[pos]
            ind = options.index(p2.dna[pos])
            del options[ind]

        for pos in range(pto_cross, dna_length): #Random
            new_city = random.choice(options)
            f3.dna[pos] = new_city
            ind = options.index(new_city)
            del options[ind]    

        #F4
        #Copia os índices de p2 após Px para f4 e o restante é completado aleatoriamente
        options = [k for k in cities]

        for pos in range(pto_cross, dna_length): #Copy
            f4.dna[pos] = p2.dna[pos]
            ind = options.index(p2.dna[pos])
            del options[ind]

        for pos in range(0, pto_cross): #Random
            new_city = random.choice(options)
            f4.dna[pos] = new_city
            ind = options.index(new_city)
            del options[ind]    

        #Calcula fitness dos novos candidatos
        f1.fitness_evaluation(resources)
        f2.fitness_evaluation(resources)   
        f3.fitness_evaluation(resources)
        f4.fitness_evaluation(resources)

        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f3)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f4)

    return np_new_pop_crossover



def create_initial_population(init_pop_qt, resources):
    if init_pop_qt <= 0:
        raise ValueError
    if resources is None:
        raise ValueError
    
    pop = []
    for pos in range(0, init_pop_qt):
        cand = Candidate(resources)
        pop.append(cand)
    return pop
    


if __name__ == '__main__':

    print("\n##################################################################")
    print("#                                                                #")
    print("#                     TSP problem                                #")
    print("#                                                                #")
    print("##################################################################")

    try:
        file_name = input("TSP problem parameters file name: ")

        if file_name is None:
            print("\nParameters file missing\n")
            raise ValueError
    
        if file_name == "":
            print("\nParameters file missing\n")
            raise ValueError
    except:
        raise ValueError

    try:
        pd_resources = pd.read_csv( file_name )
        resources = Resources( pd_resources )
    except:
        print("\nParameters load failure\n")
        exit()

    exec_init = time.time()

    search( resources )

    print(resources.get_selected_route())
    
    #Mostra tempo de execucao
    exec_end = time.time()
    diff = exec_end - exec_init	
    hours, r = divmod(diff, 3600)
    minutes, seconds = divmod(r, 60)
    print("Elapsed time: {hours:0>2}:{minutes:0>2}:{seconds:05.3f}".format(hours=int(hours), minutes=int(minutes), seconds=seconds))
