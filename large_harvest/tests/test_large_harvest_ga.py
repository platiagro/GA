# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import csv,sys
from random import uniform, randint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from large_harvest.large_harvest_ga import Step1_candidate, Step2_candidate, Resources, search_fields, search_harvesters, stop_search_step1, stop_search_step2, apply_selection, apply_mutation_step1, apply_mutation_step2, apply_crossover_step1, apply_crossover_step2, create_initial_step1_population, create_initial_step2_population


best_fit_array_full = [1]
medium_fit_array_full = [1]

pd_resources = pd.read_csv( "large_harvest/large_harvest_5_com_15.csv", sep = ';' )

resources_list_full = Resources(pd_resources)
resources_list_full.selected_fields = []
resources_list_full.selected_fields.append(1)
resources_list_full.selected_fields.append(2)
resources_list_full.selected_fields.append(3)
resources_list_full.selected_fields.append(4)
resources_list_full.selected_fields.append(5)

resources_list_full.selected_fields_x_harvesters = {1, 2, 3}

cand_step1_full = Step1_candidate(resources_list_full)
pop_step1_full = []
pop_step1_full.append(cand_step1_full)
cand_step1_pop = np.array(pop_step1_full)

cand_step2_full = Step2_candidate(resources_list_full)
pop_step2_full = []
pop_step2_full.append(cand_step2_full)
cand_step2_pop = np.array(pop_step2_full)



class TestFiles(unittest.TestCase):

    def test_resources_list__init__ok(self):
        result = Resources(pd_resources)
        self.assertNotEqual(result, "ok")
#----------------------------------------------------------
    def test_resources_list__init__blank(self):
        with self.assertRaises(ValueError):
            nova_lista = Resources(None)
#-----------------------------------------------------------            
#-----------------------------------------------------------            
    def test_cand_step1__init__blank(self):
        with self.assertRaises(ValueError):
            novo_cand = Step1_candidate(None)
#-----------------------------------------------------------
    def test_cand1_fitness_evaluation_ok(self):
        result = cand_step1_full.fitness_evaluation(resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
    def test_cand1_fitness_evaluation_blank(self):
        with self.assertRaises(ValueError):
            cand_step1_full.fitness_evaluation(None)
#-----------------------------------------------------------
#-----------------------------------------------------------        
    def test_cand_step2__init__blank(self):
        with self.assertRaises(ValueError):
            novo_cand = Step2_candidate(None)
#-----------------------------------------------------------                
    def test_cand2_fitness_evaluation_blank(self):
        with self.assertRaises(ValueError):
            cand_step2_full.fitness_evaluation(None)
#-----------------------------------------------------------
    def test_cand2_fitness_evaluation_ok(self):
        result = cand_step2_full.fitness_evaluation(resources_list_full)
        self.assertNotEqual(result, "ok")        
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_search_fields_resources_blank(self):
        with self.assertRaises(ValueError):
            search_fields(None, 500)
#-----------------------------------------------------------
    def test_search_fields_weigth_blank(self):
        with self.assertRaises(ValueError):
            search_fields(resources_list_full, 0)
#-----------------------------------------------------------
    def test_search_fields_ok(self):
        result = search_fields(resources_list_full, 500)
        self.assertEqual(result, "ok") 
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_search_harvesters_resources_blank(self):
        with self.assertRaises(ValueError):
            search_harvesters(None, 500)
#-----------------------------------------------------------    
    def test_search_harvesters_weigth_blank(self):
        with self.assertRaises(ValueError):
            search_harvesters(resources_list_full, 0)
#-----------------------------------------------------------
    def test_search_harvesters_ok(self):
        result = search_harvesters(resources_list_full, 500)
        self.assertEqual(result, "ok") 
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_stop_search_step1_weight_tolerance_blank(self):
        with self.assertRaises(ValueError): 
            stop_search_step1(0, cand_step1_pop, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step1_pop_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step1(1, None, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step1_best_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step1(1, cand_step1_pop, None, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step1_medium_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step1(1, cand_step1_pop, best_fit_array_full, None, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step1_vet_generation_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step1(1, cand_step1_pop, best_fit_array_full, medium_fit_array_full, 0, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step1_vet_products_list_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step1(1, cand_step1_pop, best_fit_array_full, medium_fit_array_full, 1, None)
#-----------------------------------------------------------
    def test_stop_search_step1_ok(self):
        result = stop_search_step1(1, cand_step1_pop, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_stop_search_step2_weight_tolerance_blank(self):
        with self.assertRaises(ValueError): 
            stop_search_step2(0, cand_step2_pop, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step2_pop_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step2(1, None, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step2_best_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step2(1, cand_step2_pop, None, medium_fit_array_full, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step2_medium_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step2(1, cand_step2_pop, best_fit_array_full, None, 1, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step2_vet_generation_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step2(1, cand_step2_pop, best_fit_array_full, medium_fit_array_full, 0, resources_list_full)
#-----------------------------------------------------------
    def test_stop_search_step2_vet_products_list_blank(self):
        with self.assertRaises(ValueError):
            stop_search_step2(1, cand_step2_pop, best_fit_array_full, medium_fit_array_full, 1, None)
#-----------------------------------------------------------
    def test_stop_search_step2_ok(self):
        result = stop_search_step2(1, cand_step2_pop, best_fit_array_full, medium_fit_array_full, 1, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_selection_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(0, cand_step1_pop)
#-----------------------------------------------------------
    def test_apply_selection_pop_intermed_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, None)
#-----------------------------------------------------------
    def test_apply_selection_ok(self):
        result = apply_selection(1, cand_step1_pop)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_mutation_step1_wished_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step1(0, cand_step1_pop, resources_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_step1_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step1(1, None, resources_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_step1_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step1(1, cand_step1_pop, None)
#-----------------------------------------------------------
    def test_apply_mutation_step1_ok(self):
        result = apply_mutation_step1(1, cand_step1_pop, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_mutation_step2_wished_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step2(0, cand_step2_pop, resources_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_step2_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step2(1, None, resources_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_step2_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation_step2(1, cand_step2_pop, None)
#-----------------------------------------------------------
    def test_apply_mutation_step2_ok(self):
        result = apply_mutation_step2(1, cand_step2_pop, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_crossover_step1_crossover_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step1(0, cand_step1_pop, resources_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_step1_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step1(1, None, resources_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_step1_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step1(1, cand_step1_pop, None)
#-----------------------------------------------------------
    def test_apply_crossover_step1_ok(self):
        result = apply_crossover_step1(1, cand_step1_pop, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_crossover_step2_crossover_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step2(0, cand_step2_pop, resources_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_step2_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step2(1, None, resources_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_step2_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover_step2(1, cand_step2_pop, None)
#-----------------------------------------------------------
    def test_apply_crossover_step2_ok(self):
        result = apply_crossover_step2(1, cand_step2_pop, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_create_initial_step1_population_init_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            create_initial_step1_population(0, resources_list_full)
#-----------------------------------------------------------
    def test_create_initial_step1_population_prod_list_blank(self):
        with self.assertRaises(ValueError):
            create_initial_step1_population(1, None)
#-----------------------------------------------------------
    def test_create_initial_step1_population_ok(self):
        result = create_initial_step1_population(1, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_create_initial_step2_population_init_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            create_initial_step2_population(0, resources_list_full)
#-----------------------------------------------------------
    def test_create_initial_step2_population_prod_list_blank(self):
        with self.assertRaises(ValueError):
            create_initial_step2_population(1, None)
#-----------------------------------------------------------
    def test_create_initial_step2_population_ok(self):
        result = create_initial_step2_population(1, resources_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
