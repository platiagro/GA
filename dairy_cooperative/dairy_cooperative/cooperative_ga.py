#Programa: cooperativa_ga.py
#Autor: Oclair Prado em mar/2020

# -*- coding: utf-8 -*-
from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
import time


class Candidate:
    np_dna = np.array( [] )
    hora = 0    #Restriction
    leite = 0   #Restriction
    margem = 0  #Benefit

    def get_hour( self ): 
        return self.hour

    def get_milk( self ): 
        return self.milk

    def get_profit( self ): 
        return self.profit

    def fitness_evaluation( self, prod_list ):
        if prod_list == None:
            raise ValueError

        self.hour = np.sum( self.np_dna * prod_list.np_hours_list )
        self.milk = np.sum( self.np_dna * prod_list.np_milk_list )
        self.profit = np.sum( self.np_dna * prod_list.np_profit_list )

    def __init__( self, prod_list ):
        if prod_list == None:
            raise ValueError

        dna = []
        tot = len( prod_list.np_hours_list )
        limite_lotes = 20  #Mais comum seria usar 1

        for pos in range( 0, tot ):
            dna.append( randint( 0, limite_lotes ) )

        np_dna_novo = np.array( dna )
        self.np_dna = np_dna_novo
        self.fitness_evaluation( prod_list )

    

class ProductsList:
    np_lista_horas = np.array( [] ) #Restriction
    np_lista_leites = np.array( [] ) #Restriction
    np_lista_margens = np.array( [] ) #Benefit

    def __init__( self, qtd_obj ):
        if qtd_obj == None:
            raise ValueError

        hours_list = []
        milk_list = []
        profit_list = []

        for pos in range( 0, qtd_obj ):
            hours_list.append( randint(1, 20) )
            milk_list.append( randint(10, 100) )
            profit_list.append( randint(10, 500) )
        
        self.np_hours_list = np.array( hours_list )
        self.np_milk_list = np.array( milk_list )
        self.np_profit_list = np.array( profit_list )    


def stop_search( hour_limit, hour_tolerance, milk_limit, milk_tolerance, population, best_fit_array, medium_fit_array, generation, prod_list ):
    if hour_limit <= 0:
        raise ValueError
    if hour_tolerance <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if milk_tolerance <= 0:
        raise ValueError
    if population == None:
        raise ValueError
    if best_fit_array == None:
        raise ValueError
    if medium_fit_array == None:
        raise ValueError
    if generation <= 0:
        raise ValueError
    if prod_list == None:
        raise ValueError

    ret = False

    best_profit = 0
    best_hour = 0
    best_milk = 0

    medium_profit = 0
    medium_hour = 0
    medium_milk = 0

    profit_amount = 0
    hour_amount = 0
    milk_amount = 0

    #Calcula fitness medio da populacao e guarda o fitness do melhor candidato
    for cand in population:
        profit_amount += cand.profit
        hour_amount += cand.hour
        milk_amount += cand.milk
        
        #Precisa pular a primeira geracao porque ainda nao foi filtrada
        if generation > 1:
            if cand.profit > best_profit:
                best_candidate = cand
                
                best_profit = cand.profit
                best_hour = cand.hour
                best_milk = cand.milk
            
                if (best_hour <= hour_limit and hour_limit - best_hour <= hour_tolerance and
                   best_milk <= milk_limit and milk_limit - best_milk <= milk_tolerance):
                    ret = True
                    #Mostra dados do melhor candidato
                    print( "hour: {0} , milk: {1} , profit: {2} , DNA: {3}".format(best_candidate.hour, best_candidate.milk, best_candidate.profit, best_candidate.np_dna ))
                    
                    print( "Hour  : {0}".format( prod_list.np_hours_list ))
                    print( "Milk  : {0}".format( prod_list.np_milk_list ))
                    print( "Profit: {0}".format( prod_list.np_profit_list ))

    if generation > 30 and best_profit == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_profit = best_fit_array[generation - 1]

    medium_hour = hour_amount / len( population )
    medium_milk = milk_amount / len( population )
    medium_profit = profit_amount / len( population )

    #Registra resultados    
    best_fit_array.append( best_profit )
    medium_fit_array.append( medium_profit )

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 30:
        if(best_candidate.hour <= hour_limit and best_candidate.milk <= milk_limit and
           best_fit_array[generation - 1] == best_fit_array[generation - 2] and
           best_fit_array[generation - 2] == best_fit_array[generation - 3] and
           best_fit_array[generation - 3] == best_fit_array[generation - 4] ):
           ret = True
           #Mostra dados do melhor candidato
           print( "hour: {0} , milk: {1} , profit: {2} , DNA: {3}".format(best_candidate.hour, best_candidate.milk, best_candidate.profit, best_candidate.np_dna ))
           
           print( "Hour  : {0}".format( prod_list.np_hours_list ))
           print( "Milk  : {0}".format( prod_list.np_milk_list ))
           print( "Profit: {0}".format( prod_list.np_profit_list ))

    #Mostra resultados
    print("Generation: {0} - Fitness [hour / milk] best: {1} [{2} / {3}] - Fitness [hour / milk] medium: {4} [{5} / {6}]".format(generation, best_profit, best_hour, best_milk, medium_profit, medium_hour, medium_milk))
    
    return ret




def search( hour_tolerance, milk_tolerance ):
    if hour_tolerance <= 0:
        raise ValueError
    if milk_tolerance <= 0:
        raise ValueError

    ini_pop_qt = 200  #Usar 1000
    intermed_pop_qt = 2000 #usar 10000
    #mutation_rate = 0.8  #Testando com 80%
    crossover_rate = 0.2 #Testando com 20%

    exec_init = time.time() 

    print("\n###################################################################")
    print("#                                                                 #")
    print("#                      Dairy cooperative problem                  #")
    print("#                                                                 #")
    print("###################################################################")

    try:
        hour_limit = int(float(input("\nWeek hour limit: ")))
        if hour_limit <= 0:
            print("\nWeek hour limit must be higher than zero!\n")
            exit()
    except:
        raise ValueError

    try:
        milk_limit = int(float(input("\nWeek milk limit: ")))
        if milk_limit <= 0:
            print("\nWeek milk limit must be higher than zero!\n")
            exit()    
    except:
        raise ValueError
    
    try:
        available_products_qt = int(float(input("\nProducts amunt to create (limit: 1010): ")))
        if available_products_qt <= 0:
            print("\nProduct amount limit should be higher than zero!\n")
            exit()
        else:    
            if available_products_qt > 1010:
                print("Amounts higher than 1010 are forbiden!")
                exit()
            elif available_products_qt <= 15:
                print("There are " + str(2 ** available_products_qt) + " possible solutions for this products amount")
            else:
                possible_solutions = 2 ** available_products_qt
                search_years = possible_solutions / (3600 * 24 * 365 * 1000000)
                print("There are {0:+5.2E} possible solutions for this products amount".format(possible_solutions))
                if available_products_qt > 44:
                    print("\nIf we had a computer capable of processing 1.000.000 candidates each second")
                    print("and considering that one year has (60s * 60m * 24h * 365d) 31.536.000 seconds")
                    print("it would take {0:+5.2e} years to find the best solution.".format(search_years))
                    print("Therefore, we'll search for just a good solution, not for the best one.")
                    print("The good solution will be the candidate with the best profit within the limit of available hours and milk in a week \n")
    except:
        raise ValueError



    prod_list = ProductsList( available_products_qt )
    populat = create_initial_population( ini_pop_qt, prod_list )
    population = sorted( populat, key = Candidate.get_profit, reverse = True )

    #print("Show the initical population: ")
    #for pos in range(0, len(population)):
    #    print("hour: {0} , profit: {1} , DNA: {2}".format(population[pos].hour, population[pos].profit, population[pos].np_dna))
    
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    #Repete este ciclo ate condicao de parada
    while not stop_search( hour_limit, hour_tolerance, milk_limit, milk_tolerance, population, best_fit_array, medium_fit_array, generation, prod_list ):
        #Cria nova população intermediaria com mutacao e crossover
        #Para manter a diversidade genetica a semente para a proxima geracao sera formada por 40% dos melhores candidatos atuais e 10% dos piores
        
        #==>Seleciona os pais para reproducao
        best_cand_qt = int(30 * ini_pop_qt / 100)
        worst_cand_qt = int(20 * ini_pop_qt / 100)
        cand_for_reproduction_1 = np.copy(population[:best_cand_qt])
        cand_for_reproduction_2 = np.copy(population[ini_pop_qt - worst_cand_qt:])
        cand_for_reproduction = np.append(cand_for_reproduction_1, cand_for_reproduction_2)
        
        #==>Reproducao por CROSSOVER
        crossover_qt = int(crossover_rate * (intermed_pop_qt - len(cand_for_reproduction)))
        if (crossover_qt % 2) != 0:
            crossover_qt = crossover_qt + 1

        intermed_pop_crossover = apply_crossover(crossover_qt, cand_for_reproduction, prod_list)
    
        #==>Reproducao por MUTAÇÃO
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>Selecao da proxima geracao de candidatos
        intermed_pop_mutation = apply_mutation(mutation_qt, cand_for_reproduction, prod_list)
    
        intermed_pop = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop = np.append(intermed_pop, intermed_pop_mutation)
        print("Size of intermed pop: {0}".format(len(intermed_pop)))

        population = apply_selection(ini_pop_qt, hour_limit, milk_limit, intermed_pop)

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
    plt.rcParams['figure.figsize'] = (8, 4)
    plt.plot(xItera, medium_fit_array, color = 'green')  #Fitness medio
    plt.scatter(xItera, best_fit_array, marker = "*", color = 'red') #Melhor fitness
    plt.title('Profit (fitness) evolution')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (profit)')
    plt.grid(True)
    plt.show()


def apply_selection(pop_qt, hour_limit, milk_limit, pop_inter):
    if pop_qt <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if pop_inter == None:
        raise ValueError
    
    #Fase 1: elimina candidatos acima do limite de hora ate limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o limite de hora
    #Remove todos acima do limite de hora ou ate que sobre somente qtd_pop
    
    #Fase 2: elimina candidatos acima do limite de leite ate limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o limite de leite
    #Remove todos acima do limite de leite ou ate que sobre somente qtd_pop

    #Fase 3: elimina candidatos com menor margem ate o limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o margem
    #Enquanto tamanho da populacao nao baixar para o tamanho desejado

    #Fase 1
    pop_sorted_by_hour = sorted( pop_inter, key = Candidate.get_hour, reverse = True)
    dismissed = True
    cand = pop_sorted_by_hour[0]
    if cand.hour > hour_limit: 
        dismissed = True
    else:
        dismissed = False

    while len(pop_sorted_by_hour) > pop_qt and dismissed == True:
        pop_sorted_by_hour = np.delete(pop_sorted_by_hour, 0)
        cand = pop_sorted_by_hour[0]
        if cand.hour > hour_limit:
            dismissed = True
        else:
            dismissed = False

    #Fase 2
    pop_sorted_by_milk = sorted( pop_inter, key = Candidate.get_milk, reverse = True)
    dismissed = True
    cand = pop_sorted_by_milk[0]
    if cand.milk > milk_limit:
        dismissed = True
    else:
        dismissed = False

    while len(pop_sorted_by_milk) > pop_qt and dismissed == True:
        pop_sorted_by_milk = np.delete(pop_sorted_by_milk, 0)
        cand = pop_sorted_by_milk[0]
        if cand.milk > milk_limit:
            dismissed = True
        else:
            dismissed = False

    #Fase 3
    pop_sorted_by_profit = sorted( pop_sorted_by_hour, key = Candidate.get_profit, reverse = True)
 
    pop_ordenada_mapop_sorted_by_profitrgem = pop_sorted_by_profit[0:pop_qt]
    
    return pop_sorted_by_profit



def apply_crossover(crossover_qt, cand_to_repro, prod_list):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro == None:
        raise ValueError
    if prod_list == None:
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
        posic_cand1 = randint(1, choice_limit)
        p1 = cand_to_repro[posic_cand1] #Seleciona p1
        #Obs.: p2 deve ser diferente de p1 para evitar perda de diversidade genetica
        posic_cand2 = randint(1, choice_limit)
        while posic_cand1 == posic_cand2: 
           posic_cand2 = randint(1, choice_limit)
        p2 = cand_to_repro[posic_cand2] #Seleciona p2

#        #Mostra DNA dos pais
#        print("[Pai 1]hora: {0} Margem: {1} DNA: {2}".format(p1.hora, p1.margem, p1.np_dna))
#        print("[Pai 2]hora: {0} Margem: {1} DNA: {2}".format(p2.hora, p2.margem, p2.np_dna))

        dna_length = len(p1.np_dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Candidate(prod_list) #DNA ja foi criado mas sera alterado por crossover
        f2 = Candidate(prod_list) #DNA tambem sera alterado
        
        #Copia parte de p1 para f1 e parte de f2 para p2
        for pos in range(0, pto_cross): #Adorei esse foreach() esquisitao
            f1.np_dna[pos] = p1.np_dna[pos]
            f2.np_dna[pos] = p2.np_dna[pos]
        
        #Copia parte de p1 para f2 e parte de p2 para f1    
        for pos in range(pto_cross, dna_length):
            f1.np_dna[pos] = p2.np_dna[pos]
            f2.np_dna[pos] = p1.np_dna[pos]
        
        #Ajusta fitness dos novos candidatos
        f1.fitness_evaluation(prod_list)
        f2.fitness_evaluation(prod_list)    
        
        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)

#        #Mostra DNA dos filhos
#        print("Ponto de crossover: " + str(pto_cross))
#        print("[Son 1]hour: {0} profit: {1} DNA: {2}".format(f1.hour, f1.profit, f1.np_dna))
#        print("[Son 2]hour: {0} profit: {1} DNA: {2}".format(f2.hour, f2.profit, f2.np_dna))

    return np_new_pop_crossover


def apply_mutation(wished_qt, cand_to_repro, prod_list):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro == None:
        raise ValueError
    if prod_list == None:
        raise ValueError

    #Cada candidato tem seu vetor de zeros e uns ( DNA[] )
    #Cada candidato selecionado gera um clone
    #Aplica mutacao no novo candidato
    
    new_pop_mutation = []
    np_new_pop_mutation = np.array( new_pop_mutation )

    for pos in range( 0, wished_qt ):
        #Seleciona aleatoriamente um membro do grupo de candidatos a reproducao
        new_cand = Candidate( prod_list )  #Este novo candidato vai receber o DNA alterado por mutacao
        choice_limit = len( cand_to_repro ) - 1
        cand_position = randint( 0, choice_limit )
        cand = cand_to_repro[cand_position]
        new_cand.np_dna = np.copy( cand.np_dna )

        #Aplica mutacao em um ponto de seu DNA
        mutation_limit = len( new_cand.np_dna ) - 1
        mutation_target = randint( 0, mutation_limit )
        if new_cand.np_dna[mutation_target] == 0:                                                                                                                
            new_cand.np_dna[mutation_target] = 1
        else:
            new_cand.np_dna[mutation_target] = 0
        
        new_cand.fitness_evaluation( prod_list )

#        #Mostra DNA do pai
#        print("[Pai]hora: {0} Margem: {1} DNA: {2}".format(cand.hora, cand.margem, cand.np_dna))
#        #Mostra DNA dos pais
#        print("[Filho]hora: {0} Margem: {1} DNA: {2}".format(novo_candidato.hora, novo_candidato.margem, novo_candidato.np_dna))
    
        #Insere novo candidato na populacao intermediaria
        np_new_pop_mutation = np.append( np_new_pop_mutation, new_cand )
        
    return np_new_pop_mutation



def create_initial_population( init_pop_qt, prod_list ):
    if init_pop_qt <= 0:
        raise ValueError
    if prod_list == None:
        raise ValueError
    
    pop = []
    for pos in range( 0, init_pop_qt ):
        cand = Candidate( prod_list )
        pop.append( cand )
    return pop
    



if __name__ == '__main__':
#    hour_tolerance = 1
#    milk_tolerance = 10

#    search( hour_tolerance = 1, milk_tolerance = 10 )
    search()
    
