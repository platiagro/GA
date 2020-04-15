# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
import time

from knapsack_problem.knapsack_ga import Candidate, ObjectsList, stop_search, search, apply_selection, apply_crossover, apply_mutation, create_initial_population


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


best_fit_array_full = [1]
medium_fit_array_full = [1]
obj_list_full = ObjectsList(20)
cand_full = Candidate(obj_list_full)
pop_full = []
pop_full.append(cand_full)
cand_pop = np.array(pop_full)

class TestFiles(unittest.TestCase):

    def test___init__blank(self):
        with self.assertRaises(ValueError):
            nova_lista = ObjectsList(None)
#-----------------------------------------------------------
    def test___init__ok(self):
        result = ObjectsList(20)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------            
#-----------------------------------------------------------    
    def test_fitness_evaluation_blank(self):
        with self.assertRaises(ValueError):
            cand_full.fitness_evaluation(None)
#-----------------------------------------------------------
    def test_fitness_evaluation_ok(self):
        result = cand_full.fitness_evaluation(obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------            
#-----------------------------------------------------------            
    def test_stop_search_weight_limit_blank(self):
        with self.assertRaises(ValueError):
            stop_search(0, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_weight_tolerance_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 0, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_pop_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, None, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_best_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, cand_pop, None, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_medium_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, cand_pop, best_fit_array_full, None, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_vet_generation_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 0, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_vet_obj_list_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, None)
#-----------------------------------------------------------
    def test_stop_search_ok(self):
            result = stop_search(1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
            self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_search_weight_tolerance_blank(self):
        with self.assertRaises(ValueError):
            search(0)
#-----------------------------------------------------------
    def test_search_ok(self):
        with self.assertRaises(ValueError):
            search(1)
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_selection_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(0, 1, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_weight_limit_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, 0, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_pop_intermed_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, 1, None)
#-----------------------------------------------------------
    def test_apply_selection_ok(self):
         result = apply_selection(1, 1, cand_pop)
         self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_crossover_crossover_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(0, cand_pop, obj_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(1, None, obj_list_full)
#-----------------------------------------------------------
    def test_apply_crossover_obj_list_blank(self):
        with self.assertRaises(ValueError):
            apply_crossover(1, cand_pop, None)
#-----------------------------------------------------------
    def test_apply_crossover_ok(self):
        result = apply_mutation(1, cand_pop, obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_mutation_wished_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(0, cand_pop, obj_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_cand_to_repro_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(1, None, obj_list_full)
#-----------------------------------------------------------
    def test_apply_mutation_obj_list_blank(self):
        with self.assertRaises(ValueError):
            apply_mutation(1, cand_pop, None)
#-----------------------------------------------------------
    def test_apply_mutation_ok(self):
        result = apply_mutation(1, cand_pop, obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_create_initial_population_init_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            create_initial_population(0, pop_full)
#-----------------------------------------------------------
    def test_create_initial_population_obj_list_blank(self):
        with self.assertRaises(ValueError):
            create_initial_population(1, None)
#-----------------------------------------------------------
    def test_create_initial_population_ok(self):
        result = create_initial_population(1, obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
