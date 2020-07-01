#Program: large_harvest_ga.py
#Author: Oclair Prado (jun/2020)

# -*- coding: utf-8 -*-
import csv,sys
from random import uniform, randint
import numpy as np
import time


class Step1_candidate:
    np_dna = np.array([])
    profit = 0             #Benefit
    #Better profit is the smallest fitness greater than zero

    def get_profit( self ): 
        return self.profit


    def fitness_evaluation( self, resources ):
        if resources is None:
            raise ValueError

        self.profit = abs( resources.grinding_harvest_limit - sum(self.np_dna * resources.np_field_harvest_capacity) )

          

    def __init__( self, resources ):
        if resources is None:
            raise ValueError

        dna = []
        tot = len( resources.np_field_harvest_capacity )
        
        for pos in range( 0, tot ):
            dna.append( randint( 0, 1 ) )

        self.np_dna = np.array( dna )
        self.fitness_evaluation( resources )


class Step2_candidate:
    np_dna = np.array([])
    profit = 0             #Benefit
    #Better profit is the smallest fitness greater than zero


    def get_profit( self ): 
        return self.profit


    def fitness_evaluation( self, resources ):
        if resources is None:
            raise ValueError
        # DNA within each position has the field index which indicates its capacities (refer to resources.np_field_harvest_capacity and resources.np_field_hour_capacity)
        # DNA position indicates the selected harvester (refer to resources.np_harvester_hour_capacity)
        
        #foreach selected field (from i to n)
            #foreach selected harvester in this field
                #sum the harvester hour capacities in hc
            #subtract hc from field hour capacity in fhc[i]
        #normalize fhc[]
        #fitness = sum(abs(fhc[]))
        
        fhc = []
        for fhc_index in resources.selected_fields:
            selected_harvest_capacity = 0
            for h_index in range(0, self.np_dna.size):
                if self.np_dna[h_index] == fhc_index:
                    selected_harvest_capacity += resources.np_harvester_hour_capacity[h_index]
            
            selected_dif = resources.np_field_hour_capacity[fhc_index] - selected_harvest_capacity
            fhc.append( selected_dif )

        np_fhc = np.array( fhc )
        np_norm_fhc = np_fhc / max( fhc )
        fitness = sum( abs( np_norm_fhc ) )

        #Check for penalties
        if min( fhc ) < 0:
            fitness = 1.2 * fitness
        #Check for bonus
            #TODO
        

        self.profit = fitness
        


    def __init__( self, resources ):
        if resources is None:
            raise ValueError

        dna = []
        tot = len( resources.np_harvester_hour_capacity )
        
        for pos in range( 0, tot ):
            next_field_index = randint( 0, len(resources.selected_fields) - 1 )
            dna.append( resources.selected_fields[next_field_index] )

        self.np_dna = np.array( dna )
        self.fitness_evaluation( resources )



class Resources:
    grinding_harvest_limit = 0   #Restriction
    
    field_id = []
    np_field_harvest_capacity = np.array( [] ) 
    np_field_hour_capacity = np.array( [] ) 
    selected_fields = []

    harvester_id = []
    np_harvester_hour_capacity = np.array( [] )   
    selected_fields_x_harvesters = []
    

    def set_selected_fields( self, best_cand ):
        self.selected_fields = []
        for pos in range( 0, best_cand.np_dna.size ):
            if best_cand.np_dna[pos] > 0:
                self.selected_fields.append( pos )


    def show_selected_fields( self ):
        print("\nSelected fields:")
        for pos in self.selected_fields:
            print("{0}: total= {1} hour= {2}".format( self.field_id[pos], self.np_field_harvest_capacity[pos], self.np_field_hour_capacity[pos] ))
        print("\n")



    def set_selected_harvesters( self, best_cand ):
        self.selected_fields_x_harvesters = best_cand.np_dna
        


    def show_selected_harvesters( self ):
        print("\n==> Selected fields x harvesters <==")
        for field_number in self.selected_fields:
            print("==> {0}: total= {1} hour= {2}".format( self.field_id[field_number], self.np_field_harvest_capacity[field_number], self.np_field_hour_capacity[field_number] ))
            if field_number in self.selected_fields_x_harvesters:
                for h_index in range(0, len( self.selected_fields_x_harvesters ) ):
                    if field_number == self.selected_fields_x_harvesters[h_index]:
                        print("=====> {0}: hour= {1}".format( self.harvester_id[h_index], self.np_harvester_hour_capacity[h_index] ))
            else:
                print("=====> none")

            print("\n")
        print("\n")



    def __init__( self, input_file_name ):
        if input_file_name == "":
            raise ValueError
        
        file_input = []
        
        field_harvest_capacity_array = []
        field_hour_capacity_array = []
        
        harvester_hour_capacity_array = []

        try:
            input_file = csv.reader(open(input_file_name), delimiter = ";")

            for [Resource, Grinding_harvest_limit, Field_harvest_capacity, Field_hour_capacity, Harvester_hour_capacity] in input_file: 
                file_input = [Resource, Grinding_harvest_limit, Field_harvest_capacity, Field_hour_capacity, Harvester_hour_capacity]
                #     0                 1                    2              3                4
                #  Resource; Grinding_harvest_limit; Field_harvest_capacity; Field_hour_capacity; Harvester_hour_capacity
                if file_input[0][0:1] != "#":
                    if file_input[0][0:4].lower() == "mill":
                        self.grinding_harvest_limit += int(file_input[1])

                    elif file_input[0][0:5].lower() == "field":
                        self.field_id.append(file_input[0])
                        field_harvest_capacity_array.append(int(file_input[2]))
                        field_hour_capacity_array.append(int(file_input[3]))

                    elif file_input[0][0:5].lower() == "harve":  
                        self.harvester_id.append(file_input[0])  
                        harvester_hour_capacity_array.append(int(file_input[4]))

                    else:
                        print("\nUnknown file resource\n")
                        raise ValueError

            self.np_field_harvest_capacity = np.array(field_harvest_capacity_array)
            self.np_field_hour_capacity = np.array(field_hour_capacity_array)

            self.np_harvester_hour_capacity = np.array(harvester_hour_capacity_array)

        except:
            print("File load failure!")
            raise ValueError
        



def search_fields( resources, weight_tolerance ):
    if resources is None:
        raise ValueError

    if weight_tolerance is None:
        raise ValueError

    if weight_tolerance <= 0:
        raise ValueError

    ini_pop_qt = 200  #hint 1000   200
    intermed_pop_qt = 1000 #hint 10000    2000
    mutation_rate = 0.4  #hint 80%
    crossover_rate = 0.6 #hint 20%

    selected_cand = np.array( [] )

    populat = create_initial_step1_population(ini_pop_qt, resources)
    population = sorted(populat, key = Step1_candidate.get_profit, reverse = False)
  
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    while not stop_search_step1( weight_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
        #==>Select parents
        best_cand_qt = int(40 * ini_pop_qt / 100)
        worst_cand_qt = int(10 * ini_pop_qt / 100)
        cand_for_reproduction_1 = np.copy(population[:best_cand_qt])
        cand_for_reproduction_2 = np.copy(population[ini_pop_qt - worst_cand_qt:])
        cand_for_reproduction = np.append(cand_for_reproduction_1, cand_for_reproduction_2)
        
        #==>CROSSOVER
        crossover_qt = int(crossover_rate * (intermed_pop_qt - len(cand_for_reproduction)))
        if (crossover_qt % 2) != 0:
            crossover_qt = crossover_qt + 1

        intermed_pop_crossover = apply_crossover_step1(crossover_qt, cand_for_reproduction, resources)
    
        #==>MUTATION
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>SELECTION
        intermed_pop_mutation = apply_mutation_step1(mutation_qt, cand_for_reproduction, resources)
    
        intermed_pop_mutation = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop_mutation = np.append(intermed_pop_mutation, intermed_pop_mutation)
        #print("Size of intermed pop: {0}".format(len(intermed_pop_mutation)))

        population = apply_selection(ini_pop_qt, intermed_pop_mutation)

        generation = generation + 1
        xItera.append(generation)
    
    print( "Fields: {0}".format( resources.selected_fields ) )
    resources.show_selected_fields()
     
    return "ok"



def search_harvesters( resources, weight_tolerance ):
    if resources is None:
        raise ValueError

    if weight_tolerance is None:
        raise ValueError

    if weight_tolerance <= 0:
        raise ValueError

    ini_pop_qt = 200  #hint 1000   200
    intermed_pop_qt = 1000 #hint 10000   2000
    mutation_rate = 0.4  #hint 80%
    crossover_rate = 0.6 #hint 20%

    selected_cand = np.array( [] )

    populat = create_initial_step2_population(ini_pop_qt, resources)
    population = sorted(populat, key = Step2_candidate.get_profit, reverse = False)
  
    generation = 1
    xItera = [1]
    best_fit_array = []
    medium_fit_array = []

    weight_tolerance = 1 # Try 1, 0 is de best
   
    while not stop_search_step2( weight_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
        #==>Select parents
        best_cand_qt = int(40 * ini_pop_qt / 100)
        worst_cand_qt = int(10 * ini_pop_qt / 100)
        cand_for_reproduction_1 = np.copy(population[:best_cand_qt])
        cand_for_reproduction_2 = np.copy(population[ini_pop_qt - worst_cand_qt:])
        cand_for_reproduction = np.append(cand_for_reproduction_1, cand_for_reproduction_2)
        
        #==>CROSSOVER 
        crossover_qt = int(crossover_rate * (intermed_pop_qt - len(cand_for_reproduction)))
        if (crossover_qt % 2) != 0:
            crossover_qt = crossover_qt + 1

        intermed_pop_crossover = apply_crossover_step2(crossover_qt, cand_for_reproduction, resources)
    
        #==>MUTATION
        mutation_qt = intermed_pop_qt - len(cand_for_reproduction) - crossover_qt
        
        #==>SELECTION
        intermed_pop_mutation = apply_mutation_step2(mutation_qt, cand_for_reproduction, resources)
    
        intermed_pop_mutation = np.append(cand_for_reproduction, intermed_pop_crossover)
        intermed_pop_mutation = np.append(intermed_pop_mutation, intermed_pop_mutation)
        #print("Size of intermed pop: {0}".format(len(intermed_pop_mutation)))

        population = apply_selection(ini_pop_qt, intermed_pop_mutation)

        #Registra parte dos resultados
        generation = generation + 1
        xItera.append(generation)
    
    resources.show_selected_harvesters()
     
    return "ok"


        
def stop_search_step1( weight_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
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
    if resources is None:
        raise ValueError

    ret = False

    best_benefit = population[0].profit
    medium_benefit = 0
    benefit_amount = 0

    if generation == 1:
        best_candidate = population[0]
   
    for cand in population:
        benefit_amount += cand.profit
        
        if cand.profit <= best_benefit:
            best_candidate = cand

            best_benefit = cand.profit
                
            if best_benefit <=  weight_tolerance:
                ret = True
                resources.set_selected_fields( cand )

    if generation > 10 and best_benefit == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_benefit = best_fit_array[generation - 1]

    medium_benefit = benefit_amount / len(population)
    
    #Registra resultados    
    best_fit_array.append(best_benefit)
    medium_fit_array.append(medium_benefit)

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 10:
        if(best_fit_array[generation - 1] == best_fit_array[generation - 2] and
           best_fit_array[generation - 2] == best_fit_array[generation - 3] and
           best_fit_array[generation - 3] == best_fit_array[generation - 4] ):
           ret = True
           best_candidate = population[0]
           resources.set_selected_fields( best_candidate )

    if ret:
        print( "Selected Fields: {0}, DNA: {1}".format(best_candidate.profit, best_candidate.np_dna))
        print( "Fields harvest capacity: {0}".format( resources.np_field_harvest_capacity ))
    else:
        print("Generation: {0} - best benefit: {1} - medium benefit: {2}".format(generation, best_benefit, medium_benefit))
    
    return ret



def stop_search_step2( weight_tolerance, population, best_fit_array, medium_fit_array, generation, resources ):
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
    if resources is None:
        raise ValueError

    ret = False

    best_benefit = population[0].profit
    medium_benefit = 0
    benefit_amount = 0

    if generation == 1:
        best_candidate = population[0]
   
    for cand in population:
        benefit_amount += cand.profit
        
        if cand.profit <= best_benefit:
            best_candidate = cand

            best_benefit = cand.profit
                
            if best_benefit <=  weight_tolerance:
                ret = True
                resources.set_selected_harvesters( cand )

    if generation > 10 and best_benefit == 0: #Nao houve melhoria nesta geracao entao repete o melhor colocado        
        best_benefit = best_fit_array[generation - 1]

    medium_benefit = benefit_amount / len(population)
    
    #Registra resultados    
    best_fit_array.append(best_benefit)
    medium_fit_array.append(medium_benefit)

    #Verifica se houve alguma alteracao nas 5 ultimas geracoes
    if generation > 10:
        if(best_fit_array[generation - 1] == best_fit_array[generation - 2] and
           best_fit_array[generation - 2] == best_fit_array[generation - 3] and
           best_fit_array[generation - 3] == best_fit_array[generation - 4] ):
           ret = True
           best_candidate = population[0]
           resources.set_selected_harvesters( best_candidate )

    if ret:
        print( "Fields x harvesters: {0}, DNA: {1}".format(best_candidate.profit, best_candidate.np_dna))
        print( "Harvester hour capacity: {0}".format( resources.np_harvester_hour_capacity ))
    else:
        print("Generation: {0} - best benefit: {1} - medium benefit: {2}".format(generation, best_benefit, medium_benefit))
    
    return ret


def apply_selection(qtd_pop, pop_inter):
    if qtd_pop <= 0:
        raise ValueError
    if pop_inter is None:
        raise ValueError
    
    #Ordena populacao intermediaria em ordem decrescente usando o beneficio
    #Enquanto tamanho da populacao nao baixar para o tamanho desejado
        #Elimina candidatos com menor beneficio ate o limite da quantidade desejada para a populacao

    pop_sorted_by_benefit = sorted( pop_inter, key = Step1_candidate.get_profit, reverse = False)
 
    pop_sorted_by_benefit = pop_sorted_by_benefit[0:qtd_pop]
    
    return pop_sorted_by_benefit




def apply_mutation_step1(wished_qt, cand_to_repro, resources):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError

    new_pop_mutation = []
    np_new_pop_mutation = np.array(new_pop_mutation)

    for pos in range(0, wished_qt):
        new_cand = Step1_candidate(resources)  
        choice_limit = len(cand_to_repro) - 1
        cand_position = randint(0, choice_limit)
        cand = cand_to_repro[cand_position]
        new_cand.np_dna = np.copy(cand.np_dna)

        mutation_limit = len(new_cand.np_dna) - 1
        mutation_target = randint(0, mutation_limit)
        if new_cand.np_dna[mutation_target] == 0:                                                                                                                
            new_cand.np_dna[mutation_target] = 1
        else:
            new_cand.np_dna[mutation_target] = 0
        
        new_cand.fitness_evaluation(resources)

        np_new_pop_mutation = np.append(np_new_pop_mutation, new_cand)
        
    return np_new_pop_mutation
    

def apply_mutation_step2(wished_qt, cand_to_repro, resources):
    if wished_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError

    new_pop_mutation = []
    np_new_pop_mutation = np.array(new_pop_mutation)

    for pos in range(0, wished_qt):
        new_cand = Step2_candidate(resources)  
        choice_limit = len(cand_to_repro) - 1
        cand_position = randint(0, choice_limit)
        cand = cand_to_repro[cand_position]
        new_cand.np_dna = np.copy(cand.np_dna)

        mutation_limit = len(new_cand.np_dna) - 1
        mutation_target = randint(0, mutation_limit)

        field_index = randint( 0, len(resources.selected_fields) -1 )
        field_number = resources.selected_fields[field_index]
        new_cand.np_dna[mutation_target] = field_number

        new_cand.fitness_evaluation(resources)

        np_new_pop_mutation = np.append(np_new_pop_mutation, new_cand)
        
    return np_new_pop_mutation


def apply_crossover_step1(crossover_qt, cand_to_repro, resources):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError
    
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

        dna_length = len(p1.np_dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Step1_candidate(resources) #DNA ja foi criado mas sera alterado por crossover
        f2 = Step1_candidate(resources) #DNA tambem sera alterado
        
        #Copia parte de p1 para f1 e parte de f2 para p2
        for pos in range(0, pto_cross): #Adorei esse foreach() esquisitao
            f1.np_dna[pos] = p1.np_dna[pos]
            f2.np_dna[pos] = p2.np_dna[pos]

        #Copia parte de p1 para f2 e parte de p2 para f1    
        for pos in range(pto_cross, dna_length):
            f1.np_dna[pos] = p2.np_dna[pos]
            f2.np_dna[pos] = p1.np_dna[pos]

        #Ajusta fitness dos novos candidatos
        f1.fitness_evaluation(resources)
        f2.fitness_evaluation(resources)   

        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)

    return np_new_pop_crossover



def apply_crossover_step2(crossover_qt, cand_to_repro, resources):
    if crossover_qt <= 0:
        raise ValueError
    if cand_to_repro is None:
        raise ValueError
    if resources is None:
        raise ValueError
    
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

        dna_length = len(p1.np_dna)
        choice_limit = dna_length - 2  #Todos os DNAs tem o mesmo tamanho e quero excluir os extremos
        pto_cross = randint(1, choice_limit) 
        
        f1 = Step2_candidate(resources) #DNA ja foi criado mas sera alterado por crossover
        f2 = Step2_candidate(resources) #DNA tambem sera alterado
        
        #Copia parte de p1 para f1 e parte de f2 para p2
        for pos in range(0, pto_cross): #Adorei esse foreach() esquisitao
            f1.np_dna[pos] = p1.np_dna[pos]
            f2.np_dna[pos] = p2.np_dna[pos]

        #Copia parte de p1 para f2 e parte de p2 para f1    
        for pos in range(pto_cross, dna_length):
            f1.np_dna[pos] = p2.np_dna[pos]
            f2.np_dna[pos] = p1.np_dna[pos]

        #Ajusta fitness dos novos candidatos
        f1.fitness_evaluation(resources)
        f2.fitness_evaluation(resources)   

        #Acrescenta novos candidatos na lista parcial  
        np_new_pop_crossover = np.append(np_new_pop_crossover, f1)
        np_new_pop_crossover = np.append(np_new_pop_crossover, f2)

    return np_new_pop_crossover



def create_initial_step1_population(init_pop_qt, resources):
    if init_pop_qt <= 0:
        raise ValueError
    if resources == None:
        raise ValueError
    
    pop = []
    for pos in range(0, init_pop_qt):
        cand = Step1_candidate(resources)
        pop.append(cand)
    return pop
    

def create_initial_step2_population(init_pop_qt, resources):
    if init_pop_qt <= 0:
        raise ValueError
    if resources == None:
        raise ValueError
    
    pop = []
    for pos in range(0, init_pop_qt):
        cand = Step2_candidate(resources)
        pop.append(cand)
    return pop





if __name__ == '__main__':
    weight_tolerance = 1 #Tonne
    resources_file_name = ""

    resources_file_name = input("\nHarvest parameters file name: ")
    if resources_file_name == "":
        print("\nParameters file missing\n")
        exit()

    try:
        resources = Resources(resources_file_name)
    except:
        print("\nParameters load failure\n")
        exit()


    try:
        weight_tolerance = int(float(input("\nHarvest weight tolerance (Ton): ")))
        if weight_tolerance <= 0:
            print("\nHarvest weight tolerance must be higher than zero!\n")
            exit()
    except:
        exit()


    exec_init = time.time()     

    print("\n##################################################################")
    print("#                                                                #")
    print("#                     Large harvest problem                      #")
    print("#                                                                #")
    print("##################################################################")
    
    search_fields( resources, weight_tolerance )  

    exec_end = time.time()
    diff = exec_end - exec_init	
    hours, r = divmod(diff, 3600)
    minutes, seconds = divmod(r, 60)
    print("\nStep 1: elapsed time: {hours:0>2}:{minutes:0>2}:{seconds:05.3f}".format(hours=int(hours), minutes=int(minutes), seconds=seconds))
    
    search_harvesters( resources, weight_tolerance )

    exec_end = time.time()
    diff = exec_end - exec_init	
    hours, r = divmod(diff, 3600)
    minutes, seconds = divmod(r, 60)
    print("\nStep 2: elapsed time: {hours:0>2}:{minutes:0>2}:{seconds:05.3f}".format(hours=int(hours), minutes=int(minutes), seconds=seconds))
    