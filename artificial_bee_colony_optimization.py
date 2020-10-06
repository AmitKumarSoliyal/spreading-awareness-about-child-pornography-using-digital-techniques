#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from igraph import Graph  
from tqdm import tqdm
from itertools import product
import itertools 
import pandas as pd
import heapq
import copy


# In[2]:


def independent_cascade_model(graph, seed_nodes, prob, n_iters):
    spread_with_seed_nodes=0
    for i in range(n_iters):
        np.random.seed(i)
        active_nodes=copy.deepcopy(seed_nodes)
        active_nodes=list(set(active_nodes))
        newly_active_nodes=copy.deepcopy(seed_nodes)
        while len(newly_active_nodes)>0:
            activated_nodes=[]
            for node in newly_active_nodes:
                neighbors=graph.neighbors(node,mode='out')
                success=np.random.uniform(0,1,len(neighbors))<prob
                activated_nodes+=list(np.extract(success, neighbors))
            activated_nodes=list(set(activated_nodes))#remove duplicate nodes
            newly_active_nodes=list(set(activated_nodes)-set(active_nodes))
            active_nodes+=newly_active_nodes
        spread_with_seed_nodes+=len(active_nodes)
        #print(i,' spread_with_seed_nodes: ',spread_with_seed_nodes)
    return (spread_with_seed_nodes/ n_iters)*100/graph.vcount()


# In[3]:


class bee:
    def __init__(self,graph, k, prob, n_iters):
        self.food_source=list(random.sample(list(range(graph.vcount())), k))  #solution
        self.objective_function=independent_cascade_model(graph, self.food_source, prob, n_iters)
        self.fitness=calculate_fitness(self.objective_function)
        self.trial=0
    
    


# In[4]:


def generate_random_solution(number_of_food_sources,graph, k, prob, n_iters):
    population=[]
    for i in range(number_of_food_sources):
        population.append(bee(graph, k, prob, n_iters))
    return population


# In[5]:


def calculate_fitness(objective_function):
    if objective_function>=0:
        return -1*(1/(1+objective_function))
    else:
        return -1*(1+math.abs(objective_function))


# In[6]:


def bound_check(new_food,lb,ub):
    if new_food< lb:
        return 0
    if new_food>ub:
        return ub-1
    return int(new_food)
    


# In[7]:


def algo(graph, k, prob, n_iters):
    start_time = time.time()
#     print('Initialization')
    swarm_size=100
    number_of_cycles=20
    limit=int(swarm_size/2+k)
    number_of_employeed_bees=int(swarm_size/2)
    number_of_onlooker_bees=int(swarm_size/2)
    number_of_food_sources=int(swarm_size/2)
    population=generate_random_solution(number_of_food_sources,graph, k, prob, n_iters)
#    for i in range(number_of_food_sources):
#         #print(population[i].food_source,'\t\t\t\t',population[i].objective_function,'\t',population[i].fitness,'\t',population[i].tria#l)
#    print('Employeed bee phase')
    for cycles in tqdm(range(number_of_cycles)):
        ##employeed bee phase
        for i in range(number_of_food_sources):
            random_point=random.randint(0,len(population[i].food_source)-1)
            random_partner=random.randint(0,number_of_food_sources-1)
            fi=random.uniform(-1, 1)
#             print('random_point: ',random_point,' random_partner: ',random_partner,' fi: ',fi)
            new_food=population[i].food_source[random_point]+fi*(population[i].food_source[random_point]-population[random_partner].food_source[random_point])
#             print('new food:',new_food)
            new_food=bound_check(new_food,0,graph.vcount()-1)
#             print('new food:',new_food)
            new_food_source=bee(graph, k, prob, n_iters)
            new_food_source.food_source=copy.deepcopy(population[i].food_source)
            new_food_source.food_source[random_point]=new_food
            new_food_source.objective_function=independent_cascade_model(graph, new_food_source.food_source, prob, n_iters)
            new_food_source.fitness=calculate_fitness(new_food_source.objective_function)
            new_food_source.trial=0
            if new_food_source.fitness<population[i].fitness:
                population[i]=new_food_source
                population[i].trial=0
            else:
                population[i].trial+=1
#        for i in range(number_of_food_sources):
#             print(population[i].food_source,'\t\t\t\t',population[i].objective_function,'\t',population[i].fitness,'\t',population[i].trial)
        ##onlooker phase
#         print('Onlooker bee phase')
        probability=[]
        tmp=[]
        for i in range(number_of_food_sources):
            tmp.append(population[i].fitness)
        max_fitness=max(tmp)
        for i in range(number_of_food_sources):
            probability.append(0.9*(population[i].fitness/max_fitness)+0.1)
        for i in range(number_of_food_sources):
            if probability[i]>random.uniform(0, 1):
                random_point=random.randint(0,len(population[i].food_source)-1)
                random_partner=random.randint(0,number_of_food_sources-1)
                fi=random.uniform(-1, 1)
#                 print('random_point: ',random_point,' random_partner: ',random_partner,' fi: ',fi)
                new_food=population[i].food_source[random_point]+fi*(population[i].food_source[random_point]-population[random_partner].food_source[random_point])
#                 print('new food:',new_food)
                new_food=bound_check(new_food,0,graph.vcount()-1)
#                 print('new food:',new_food)
                new_food_source=bee(graph, k, prob, n_iters)
                new_food_source.food_source=copy.deepcopy(population[i].food_source)
                new_food_source.food_source[random_point]=new_food
                new_food_source.objective_function=independent_cascade_model(graph, new_food_source.food_source, prob, n_iters)
                new_food_source.fitness=calculate_fitness(new_food_source.objective_function)
                new_food_source.trial=0
                if new_food_source.fitness>population[i].fitness:
                    population[i]=new_food_source
                    population[i].trial=0
                else:
                    population[i].trial+=1
#        for i in range(number_of_food_sources):
#             print(population[i].food_source,'\t\t\t\t',population[i].objective_function,'\t',population[i].fitness,'\t',population[i].trial)
        ##scout Phase
#         print('Scout bee Phase')
        best_solution=population[0]
        for i in range(1,number_of_food_sources):
            if best_solution.fitness<population[i].fitness:
                best_solution=copy.deepcopy(population[i])
#         print('Best solution')
#         print(best_solution.food_source,'\t\t\t\t',best_solution.objective_function,'\t',best_solution.fitness,'\t',best_solution.trial)
        for i in range(1,number_of_food_sources):
            if population[i].trial>limit:
                population[i]=bee(graph, k, prob, n_iters) ##new random solution
#        for i in range(number_of_food_sources):
#             print(population[i].food_source,'\t\t\t\t',population[i].objective_function,'\t',population[i].fitness,'\t',population[i].trial)
#         print('#######################')
    best_solution=population[0]
    for i in range(1,number_of_food_sources):
        if best_solution.fitness<population[i].fitness:
            best_solution=copy.deepcopy(population[i])
    end_time=time.time()
    return best_solution.food_source,best_solution.objective_function,round(end_time-start_time, 2)


# In[ ]:





# In[ ]:





# In[8]:








