# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

import csv,sys
from random import uniform, randint
import numpy as np
import matplotlib.pyplot as plt
import time

from dairy_cooperative.cooperative_ga_CSV import Candidate, ProductsList, stop_search, load_csv_file, search, apply_selection, apply_crossover, apply_mutation, create_initial_population


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





best_fit_array_full = [1]
medium_fit_array_full = [1]
obj_list_full = ProductsList(20)
cand_full = Candidate(obj_list_full)
pop_full = []
pop_full.append(cand_full)
cand_pop = np.array(pop_full)




class TestFiles(unittest.TestCase):

    def test___init__ok(self):
        result = ProductsList(20)
        self.assertNotEqual(result, "ok")
#----------------------------------------------------------
    def test___init__blank(self):
        with self.assertRaises(ValueError):
            nova_lista = ProductsList(None)
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
    def test_stop_search_hour_limit_blank(self):
        with self.assertRaises(ValueError):
            stop_search(0, 1, 1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_hour_tolerance_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 0, 1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_milk_limit_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 0, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_milk_tolerance_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 0, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_pop_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 1, None, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_best_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 1, cand_pop, None, medium_fit_array_full, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_medium_fit_array_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 1, pop_full, best_fit_array_full, None, 1, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_vet_generation_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 0, obj_list_full)
#-----------------------------------------------------------
    def test_stop_search_vet_products_list_blank(self):
        with self.assertRaises(ValueError):
            stop_search(1, 1, 1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, None)
#-----------------------------------------------------------
    def test_stop_search_ok(self):
        result = stop_search(1, 1, 1, 1, cand_pop, best_fit_array_full, medium_fit_array_full, 1, obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_load_csv_file_name_blank(self):
        with self.assertRaises(ValueError):
            load_csv_file("")
#-----------------------------------------------------------
    def test_load_csv_file_ok(self):
       result = load_csv_file("file_name.csv")
       self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_search_hour_tolerance_blank(self):
        with self.assertRaises(ValueError):
            search(0, 1, "file_name.csv")
#-----------------------------------------------------------
    def test_search_milk_tolerance_blank(self):
        with self.assertRaises(ValueError):
            search(1, 0, "file_name.csv")
#-----------------------------------------------------------
    def test_search_prod_file_name_blank(self):
        with self.assertRaises(ValueError):
            search(1, 1, "")
#-----------------------------------------------------------
    def test_search_ok(self):
        with self.assertRaises(ValueError):
            search(1, 1, "file_name.csv")
#-----------------------------------------------------------
#-----------------------------------------------------------
    def test_apply_selection_pop_qt_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(0, 1, 1, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_hour_limit_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, 0, 1, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_milk_limit_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, 1, 0, cand_pop)
#-----------------------------------------------------------
    def test_apply_selection_pop_intermed_blank(self):
        with self.assertRaises(ValueError):
            apply_selection(1, 1, 1, None)
#-----------------------------------------------------------
    def test_apply_selection_ok(self):
        result = apply_selection(1, 1, 1, cand_pop)
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
    def test_apply_crossover_prod_list_blank(self):
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
    def test_apply_mutation_prod_list_blank(self):
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
            create_initial_population(0, obj_list_full)
#-----------------------------------------------------------
    def test_create_initial_population_prod_list_blank(self):
        with self.assertRaises(ValueError):
            create_initial_population(1, None)
#-----------------------------------------------------------
    def test_create_initial_population_ok(self):
        result = create_initial_population(1, obj_list_full)
        self.assertNotEqual(result, "ok")
#-----------------------------------------------------------
#-----------------------------------------------------------
