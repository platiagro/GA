#Programa: cooperativa_ga_CSV.py
#Autor: Oclair Prado em mar/2020

# -*- coding: utf-8 -*-
import csv,sys
from random import uniform, randint
import numpy as np
import pandas as pd
import time


class Candidate:
    np_dna = np.array([])
    hour = 0    #Restriction
    milk = 0    #Restriction
    profit = 0  #Benefit
    fitness = 0 

    def get_hour( self ): 
        return self.hour

    def get_milk( self ): 
        return self.milk

    def get_profit( self ): 
        return self.profit

    def get_fitness( self ):
        return self.fitness

    def fitness_evaluation( self, milk_limit, hour_limit, prod_list ):
        if milk_limit <= 0:
            raise ValueError
        if hour_limit <= 0:
            raise ValueError
        if prod_list is None:
            raise ValueError

        self.hour = np.sum( self.np_dna * prod_list.np_hours_list )
        self.milk = np.sum( self.np_dna * prod_list.np_milk_list )
        self.profit = np.sum( self.np_dna * prod_list.np_profit_list )
        milk_step = milk_limit - self.milk
        if milk_step < 0:
            milk_step = -10 * milk_step
        
        hour_step = hour_limit - self.hour
        if hour_step < 0:
            hour_step = -10 * hour_step

        self.fitness = self.profit - milk_step - hour_step
    

    def __init__( self, milk_limit, hour_limit, prod_list ):
        if milk_limit <= 0:
            raise ValueError
        if hour_limit <= 0:
            raise ValueError
        if prod_list is None:
            raise ValueError

        dna = []
        tot = len( prod_list.np_hours_list )
        lots_limit = 1  #Mais comum seria usar 1

        for pos in range( 0, tot ):
            dna.append( randint( 0, lots_limit ) )

        np_dna_new = np.array( dna )
        self.np_dna = np_dna_new
        self.fitness_evaluation( milk_limit, hour_limit, prod_list )

    

class ProductsList:
    np_products_list = np.array( [] ) #Produtcs
    np_milk_list = np.array( [] )   #Restriction
    np_hours_list = np.array( [] )  #Restriction
    np_profit_list = np.array( [] ) #Benefit
    np_selected_products = np.array( [] )


    def set_selected_products( self, candidate ):
        if candidate is None:
            raise ValueError

        self.np_selected_products = candidate.np_dna


    def get_selected_products( self ):
        response = {}
        #| Prod | Qtd | Milk | Hour | Profit |
        acum_milk = 0
        acum_hours = 0
        acum_profit = 0

        column_product_name = "Produto"
        column_product = []
        column_qtd_name = "Qtd"
        column_qtd = []
        column_milk_name = "Leite"
        column_milk = []
        column_hour_name = "Hora"
        column_hour = []
        column_profit_name = "Margem"
        column_profit = []
        
        qtd = self.np_selected_products.shape[0]
        for pos in range( 0, qtd ):
            if self.np_selected_products[pos] > 0:
                column_product.append( self.np_products_list[pos] )
                column_qtd.append( self.np_selected_products[pos] )
                column_milk.append( self.np_milk_list[pos] )
                acum_milk += self.np_milk_list[pos]
                column_hour.append( self.np_hours_list[pos] )
                acum_hours += self.np_hours_list[pos]
                column_profit.append( self.np_profit_list[pos] )
                acum_profit += self.np_profit_list[pos]

        column_product.append( "" )
        column_qtd.append( "" )
        column_milk.append( acum_milk )
        column_hour.append( acum_hours )
        column_profit.append( acum_profit )

        response[column_product_name] = column_product
        response[column_qtd_name] = column_qtd
        response[column_milk_name] = column_milk
        response[column_hour_name] = column_hour
        response[column_profit_name] = column_profit
                         
        pd_response = pd.DataFrame( data = response )
        return pd_response


    def __init__( self, pd_resources ):
        if pd_resources is None:
            raise ValueError

        products_List = []
        milk_list = []
        hours_list = []
        profit_list = []

        try:
            for index in pd_resources.itertuples():
                if index[1][0:1].lower() != "#":
                    #     0      1     2      3
                    #  Product, milk, hour, profit
                    products_List.append(index[1])
                    milk_list.append(int(index[2]))
                    hours_list.append(int(index[3]))
                    profit_list.append(int(index[4]))

            self.np_products_list = np.array(products_List)
            self.np_milk_list = np.array(milk_list)
            self.np_hours_list = np.array(hours_list)
            self.np_profit_list = np.array(profit_list)

        except Exception as inst:
            print(inst)
            print("File load failure!")
            raise ValueError
          

def stop_search( hour_limit, hour_tolerance, milk_limit, milk_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
    if hour_limit <= 0:
        raise ValueError
    if hour_tolerance <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if milk_tolerance <= 0:
        raise ValueError
    if population is None:
        raise ValueError
    if best_fit_array is None:
        raise ValueError
    if medium_fit_array is None:
        raise ValueError
    if generation <= 0:
        raise ValueError
    if resources is None:
        raise ValueError

    if generation == 0:
        return False

    ret = False

    best_fitness = 0
    best_hour = 0
    best_milk = 0

    medium_fitness = 0
    medium_hour = 0
    medium_milk = 0

    fitness_amount = 0
    hour_amount = 0
    milk_amount = 0

    #Calcula fitness medio da populacao e guarda o fitness do melhor candidato
    pop_sorted_by_fitness = sorted( population, key = Candidate.get_fitness, reverse = True)
    best_candidate = pop_sorted_by_fitness[0]
    best_fitness = best_candidate.fitness
    best_hour = best_candidate.hour
    best_milk = best_candidate.milk

    for cand in pop_sorted_by_fitness:
        fitness_amount += cand.fitness
        hour_amount += cand.hour
        milk_amount += cand.milk
                
        #Precisa pular a primeira geracao porque ainda nao foi filtrada
        if generation > 1:

            if cand.fitness >= best_fitness:
                best_candidate = cand
                
                best_fitness = cand.fitness
                best_hour = cand.hour
                best_milk = cand.milk
                            
                if( best_hour <= hour_limit and (hour_limit - best_hour) <= hour_tolerance and
                    best_milk <= milk_limit and (milk_limit - best_milk) <= milk_tolerance ):
                    ret = True
                    resources.set_selected_products( cand )
                    #Mostra dados do melhor candidato
                    print("")
                    print( "fitness: {0} , hour: {1} , milk: {2} , profit: {3} , DNA: {4}".format(best_candidate.fitness, best_candidate.hour, best_candidate.milk, best_candidate.profit, best_candidate.np_dna ))
                    
                    print( "Hour  : {0}".format( resources.np_hours_list ))
                    print( "Milk  : {0}".format( resources.np_milk_list ))
                    print( "Profit: {0}".format( resources.np_profit_list ))
                    return True

    if generation > 30 and best_fitness == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_fitness = best_fit_array[generation - 2]

    medium_hour = hour_amount / len( population )
    medium_milk = milk_amount / len( population )
    medium_fitness = fitness_amount / len( population )

    #Registra resultados    
    best_fit_array.append( best_fitness )
    medium_fit_array.append( medium_fitness )

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 30:
        if best_candidate.hour <= hour_limit and best_candidate.milk <= milk_limit:
            if best_fit_array[generation - 2] == best_fit_array[generation - 3]:
                if best_fit_array[generation - 3] == best_fit_array[generation - 4]:
                    if best_fit_array[generation - 4] == best_fit_array[generation - 5]:
                        ret = True
                        resources.set_selected_products( best_candidate )
                        #Mostra dados do melhor candidato
                        print("")
                        print( "fitness: {0} , hour: {1} , milk: {2} , profit: {3} , DNA: {4}".format(best_candidate.fitness, best_candidate.hour, best_candidate.milk, best_candidate.profit, best_candidate.np_dna ))
           
                        print( "Hour  : {0}".format( resources.np_hours_list ))
                        print( "Milk  : {0}".format( resources.np_milk_list ))
                        print( "Profit: {0}".format( resources.np_profit_list ))

    #Mostra resultados
    print("Generation: {0} - Fitness [hour / milk] best: {1} [{2} / {3}] - Fitness [hour / milk] medium: {4} [{5} / {6}]".format(generation, best_fitness, best_hour, best_milk, medium_fitness, medium_hour, medium_milk))
    
    return ret




def search( hour_tolerance, hour_limit, milk_tolerance, milk_limit, resources ):
    if hour_tolerance <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if milk_tolerance <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if resources is None:
        raise ValueError

    ini_pop_qt = 200  #Usar 1000
    intermed_pop_qt = 2000 #usar 10000
    #mutation_rate = 0.2  #Testando com 80%
    crossover_rate = 0.8 #Testando com 20%

    if len(resources.np_products_list) < 2:
        print("\nProducts not found. Using random option")
        available_products_qt = int(float(input("\nProducts amunt to create (limit: 1010): ")))
    else:
        available_products_qt = len(resources.np_products_list) - 1

    if available_products_qt <= 0:
        print("\nProduct amount limit should be higher than zero!\n")
        exit()
        
    if available_products_qt > 1010:
        print("Amounts higher than 1010 are forbiden!")
        exit()

    if available_products_qt <= 15:
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

    populat = create_initial_population( ini_pop_qt, milk_limit, hour_limit, resources )
    population = sorted( populat, key = Candidate.get_profit, reverse = True )

    #print("Show the initical population: ")
    #for pos in range(0, len(population)):
    #    print("hour: {0} , profit: {1} , DNA: {2}".format(population[pos].hour, population[pos].profit, population[pos].np_dna))
    
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    #Repete este ciclo ate condicao de parada
    while not stop_search( hour_limit, hour_tolerance, milk_limit, milk_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
        #Cria nova populacao intermediaria com mutacao e crossover
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

        intermed_pop_crossover = apply_crossover(crossover_qt, cand_for_reproduction, milk_limit, hour_limit, resources)
    
        #==>Reproducao por MUTACAO
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>Selecao da proxima geracao de candidatos
        intermed_pop_mutation = apply_mutation(mutation_qt, cand_for_reproduction, milk_limit, hour_limit, resources)
    
        intermed_pop = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop = np.append(intermed_pop, intermed_pop_mutation)
        #print("Size of intermed pop: {0}".format(len(intermed_pop)))

        population = apply_selection(ini_pop_qt, hour_limit, milk_limit, intermed_pop)

        #Registra parte dos resultados
        generation = generation + 1
        xItera.append(generation)

   


def apply_selection(pop_qt, hour_limit, milk_limit, pop_inter):
    if pop_qt <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if pop_inter is None:
        raise ValueError
    
    #Fase 1: elimina candidatos acima do limite de hora ate limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o limite de hora
    #Remove todos acima do limite de hora ou ate que sobre somente qtd_pop
    pop_sorted_by_hour = sorted( pop_inter, key = Candidate.get_hour, reverse = True)
    dismissed = True
    while len(pop_sorted_by_hour) > pop_qt and dismissed == True:
        pop_sorted_by_hour = np.delete(pop_sorted_by_hour, 0)
        cand = pop_sorted_by_hour[0]
        if cand.hour > hour_limit:
            dismissed = True
        else:
            dismissed = False

    #Fase 2: elimina candidatos acima do limite de leite ate limite da quantidade desejada para a populacao
    #Ordena populacao intermediaria em ordem decrescente usando o limite de leite
    #Remove todos acima do limite de leite ou ate que sobre somente qtd_pop
    pop_sorted_by_milk = sorted( pop_sorted_by_hour, key = Candidate.get_milk, reverse = True)
    dismissed = True
    while len(pop_sorted_by_milk) > pop_qt and dismissed == True:
        pop_sorted_by_milk = np.delete(pop_sorted_by_milk, 0)
        cand = pop_sorted_by_milk[0]
        if cand.milk > milk_limit:
            dismissed = True
        else:
            dismissed = False

    #Fase 3: elimina candidatos ate o limite da quantidade desejada para a populacao
    pop_sorted_by_fitness = sorted( pop_sorted_by_milk, key = Candidate.get_fitness, reverse = True)
    pop_sorted_by_fitness_sharp = pop_sorted_by_fitness[0:pop_qt]
    
    return pop_sorted_by_fitness_sharp



def apply_crossover(crossover_qt, cand_to_repro, milk_limit, hour_limit, prod_list):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if prod_list is None:
        raise ValueError

    #A crossover_qt indica a quantidade de descendentes a ser produzida
    #Em cada ciclo sao criados dois novos descendentes
    #Entao serao realizados "crossover_qt/2" ciclos
    #Em cada ciclo:
        #Seleciona 2 pais da lista de candidatos a reproducao, p1 e p2
        #Seleciona ponto de crossover
        #Cria dois novos candidatos, f1 e f2
        #Copia DNA de p1 ate o ponto de crossover para o inicio de f1
        #Copia DNA de p1 apos o ponto de crossover para o fim de f2
        #Copia DNA de p2 ate o ponto de crossover para o inicio de f2
        #Copia DNA de p2 apos o ponto de crossover para o fim de f1
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
#        print("[Father 1]hour: {0} profit: {1} DNA: {2}".format(p1.hour, p1.profit, p1.np_dna))
#        print("[Father 2]hour: {0} profit: {1} DNA: {2}".format(p2.hour, p2.profit, p2.np_dna))

        dna_length = len(p1.np_dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Candidate(milk_limit, hour_limit, prod_list) #DNA ja foi criado mas sera alterado por crossover
        f2 = Candidate(milk_limit, hour_limit, prod_list) #DNA tambem sera alterado
        
        #Copia parte de p1 para f1 e parte de f2 para p2
        for pos in range(0, pto_cross): #Adorei esse foreach() esquisitao
            f1.np_dna[pos] = p1.np_dna[pos]
            f2.np_dna[pos] = p2.np_dna[pos]
        
        #Copia parte de p1 para f2 e parte de p2 para f1    
        for pos in range(pto_cross, dna_length):
            f1.np_dna[pos] = p2.np_dna[pos]
            f2.np_dna[pos] = p1.np_dna[pos]
        
        #Ajusta fitness dos novos candidatos
        f1.fitness_evaluation( milk_limit, hour_limit, prod_list )
        f2.fitness_evaluation( milk_limit, hour_limit, prod_list )    
        
        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)

#        #Mostra DNA dos filhos
#        print("Ponto de crossover: " + str(pto_cross))
#        print("[Son 1]hour: {0} profit: {1} DNA: {2}".format(f1.hour, f1.profit, f1.np_dna))
#        print("[Son 2]hour: {0} profit: {1} DNA: {2}".format(f2.hour, f2.profit, f2.np_dna))

    return np_new_pop_crossover


def apply_mutation(wished_qt, cand_to_repro, milk_limit, hour_limit, prod_list):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if prod_list is None:
        raise ValueError

    #Cada candidato tem seu vetor de zeros e uns ( DNA[] )
    #Cada candidato selecionado gera um clone
    #Aplica mutacao no novo candidato
    
    new_pop_mutation = []
    np_new_pop_mutation = np.array( new_pop_mutation )

    for pos in range( 0, wished_qt ):
        #Seleciona aleatoriamente um membro do grupo de candidatos a reproducao
        new_cand = Candidate( milk_limit, hour_limit, prod_list )  #Este novo candidato vai receber o DNA alterado por mutacao
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
        
        new_cand.fitness_evaluation( milk_limit, hour_limit, prod_list )

#        #Mostra DNA do pai
#        print("[Father]hour: {0} profit: {1} DNA: {2}".format(cand.hour, cand.profit, cand.np_dna))
#        #Mostra DNA dos pais
#        print("[Son]hour: {0} profit: {1} DNA: {2}".format(new_cand.hour, new_cand.profit, new_cand.np_dna))
    
        #Insere novo candidato na populacao intermediaria
        np_new_pop_mutation = np.append( np_new_pop_mutation, new_cand )
        
    return np_new_pop_mutation
    


def create_initial_population( init_pop_qt, milk_limit, hour_limit, prod_list ):
    if init_pop_qt <= 0:
        raise ValueError
    if milk_limit <= 0:
        raise ValueError
    if hour_limit <= 0:
        raise ValueError
    if prod_list is None:
        raise ValueError
    
    pop = []
    for pos in range( 0, init_pop_qt ):
        cand = Candidate( milk_limit, hour_limit, prod_list )
        pop.append( cand )
    return pop
    



if __name__ == '__main__':
    hour_tolerance = 2
    milk_tolerance = 50
    resources_file_name = ""

    print("\n###################################################################")
    print("#                                                                 #")
    print("#                      Dairy cooperative problem                  #")
    print("#                                                                 #")
    print("###################################################################")


    resources_file_name = input("\nDairy parameters file name: ")
    if resources_file_name == "":
        print("\nParameters file missing\n")
        exit()

    try:
        pd_resources = pd.read_csv( resources_file_name )
        resources = ProductsList( pd_resources )
    except:
        print("\nParameters load failure\n")
        exit()

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


    exec_init = time.time()  

    search( hour_tolerance, hour_limit, milk_tolerance, milk_limit, resources )
    
    print( resources.get_selected_products())

    exec_end = time.time()
    diff = exec_end - exec_init	
    hours, r = divmod(diff, 3600)
    minutes, seconds = divmod(r, 60)
    print("\nElapsed time: {hours:0>2}:{minutes:0>2}:{seconds:05.3f}".format(hours=int(hours), minutes=int(minutes), seconds=seconds))
    