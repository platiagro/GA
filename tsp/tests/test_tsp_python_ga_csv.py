# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import random
from random import uniform, randint
import numpy as np
import pandas as pd
import time

from tsp.tsp_python_ga_csv import Candidate, Resources, stop_search, search, apply_selection, apply_crossover, apply_mutation, create_initial_population


#------------------------------------------------
dict_dist = {'Origem': ['Cidade_001', 'Cidade_001', 'Cidade_001', 'Cidade_002', 'Cidade_002', 'Cidade_002', 'Cidade_003', 'Cidade_003', 'Cidade_003', 'Cidade_004', 'Cidade_004','Cidade_004'], 'Destino': ['Cidade_002', 'Cidade_003','Cidade_004', 'Cidade_001', 'Cidade_003', "Cidade_004", 'Cidade_001', 'Cidade_002', 'Cidade_004', 'Cidade_001', 'Cidade_002', 'Cidade_003'], 'KM':[1,2, 3, 1, 4, 5, 2, 4, 6, 3, 5, 6]}
pd_dict = pd.DataFrame(data = dict_dist)
#------------------------------------------------

resource = Resources(pd_dict)
cand_full = Candidate( resource )

best_fit_array_full = [1]
medium_fit_array_full = [1]
pop_full = [cand_full]
cand_pop = np.array(pop_full)


class TestFiles(unittest.TestCase):
#----------------------------------------------------------
    def test_resources__init__blank(self):
        with self.assertRaises(ValueError):
            nova_lista = Resources(None)
#-----------------------------------------------------------
    def test_resources__init__ok(self):
        result = Resources(resource)
        self.assertNotEqual(result, "ok")    
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_cand__init__blank(self):
        with self.assertRaises(ValueError):
            novo_cand = Candidate(None)
#-----------------------------------------------------------
    def test_cand__init__ok(self):
        result = Candidate( resource )
        self.assertNotEqual( result, "ok" )
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_fitness_evaluation_blank(self):
        with self.assertRaises(ValueError):
            cand_full.fitness_evaluation(None)
#-----------------------------------------------------------
    def test_fitness_evaluation_ok(self):
        result = cand_full.fitness_evaluation(resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_generate_dna_blank(self):
        with self.assertRaises(ValueError):
            cand_full.generate_dna(None)
#-----------------------------------------------------------
    def test_generate_dna_ok(self):
        result = cand_full.generate_dna(resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_search_resources_blank(self):
        with self.assertRaises(ValueError):
            search(None)
#-----------------------------------------------------------
    def test_search_ok(self):
        with self.assertRaises(ValueError):
            search(resource)
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_stop_search_pop_blank(self):
        with self.assertRaises(ValueError):
            stop_search(None, best_fit_array_full, medium_fit_array_full, 1, resource)
#-----------------------------------------------------------
    def test_stop_search_best_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(cand_pop, None, medium_fit_array_full, 1, resource)
#-----------------------------------------------------------
    def test_stop_search_medium_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(cand_pop, best_fit_array_full, None, 1, resource)
#-----------------------------------------------------------
    def test_stop_search_vet_generation_blank(self):
        with self.assertRaises(ValueError):
            stop_search(cand_pop, best_fit_array_full, medium_fit_array_full, 0, resource)
#-----------------------------------------------------------
    def test_stop_search_vet_generation_neg(self):
        with self.assertRaises(ValueError):
            stop_search(cand_pop, best_fit_array_full, medium_fit_array_full, -1, resource)
#-----------------------------------------------------------
    def test_stop_search_vet_products_list_blank(self):
        with self.assertRaises(ValueError):
            stop_search(cand_pop, best_fit_array_full, medium_fit_array_full, 1, None)
#-----------------------------------------------------------
    def test_stop_search_ok(self):
        result = stop_search(cand_pop, best_fit_array_full, medium_fit_array_full, 1, resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_selection_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(0, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_pop_qt_neg(self):
        with self.assertRaises(ValueError):
            apply_selection(-1, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_pop_intermed_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, None)
#-----------------------------------------------------------
    def test_apply_selection_ok(self):
        result = apply_selection(1, cand_pop)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_mutation_wished_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(0, cand_pop, resource)
#-----------------------------------------------------------
    def test_apply_mutation_wished_qt_neg(self):
        with self.assertRaises(ValueError):
            apply_mutation(-1, cand_pop, resource)
#-----------------------------------------------------------
    def test_apply_mutation_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(1, None, resource)
#-----------------------------------------------------------
    def test_apply_mutation_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(1, cand_pop, None)
#-----------------------------------------------------------
    def test_apply_mutation_ok(self):
        result = apply_mutation(1, cand_pop, resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_crossover_crossover_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(0, cand_pop, resource)
#-----------------------------------------------------------
    def test_apply_crossover_crossover_qt_neg(self):
        with self.assertRaises(ValueError):
            apply_crossover(-1, cand_pop, resource)
#-----------------------------------------------------------
    def test_apply_crossover_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(1, None, resource)
#-----------------------------------------------------------          
    def test_apply_crossover_prod_list_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(1, cand_pop, None)
#-----------------------------------------------------------
    def test_apply_crossover_ok(self):
        result = apply_mutation(1, cand_pop, resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_create_initial_population_init_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            create_initial_population(0, resource)
#-----------------------------------------------------------
    def test_create_initial_population_init_pop_qt_neg(self):
        with self.assertRaises(ValueError):
            create_initial_population(-1, resource)
#-----------------------------------------------------------
    def test_create_initial_population_prod_list_blank(self):
        with self.assertRaises(ValueError):
            create_initial_population(1,None)
#-----------------------------------------------------------
    def test_create_initial_population_ok(self):
        result = create_initial_population(1,resource)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
