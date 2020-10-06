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


def independent_cascade_model(graph, seed_nodes, prob,n_iters,u):
    
    spread_with_seed_nodes=0
    spread_with_seed_nodes_and_u=0
    for i in range(n_iters):
        np.random.seed(i)
        active_nodes=copy.deepcopy(seed_nodes)
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
        newly_active_nodes=[u]
        while len(newly_active_nodes)>0:
            activated_nodes=[]
            for node in newly_active_nodes:
                neighbors=graph.neighbors(node,mode='out')
                success=np.random.uniform(0,1,len(neighbors))<prob
                activated_nodes+=list(np.extract(success, neighbors))
            activated_nodes=list(set(activated_nodes))#remove duplicate nodes
            newly_active_nodes=list(set(activated_nodes)-set(active_nodes))
            active_nodes+=newly_active_nodes
        spread_with_seed_nodes_and_u+=len(active_nodes)
        #print(i,' spread_with_seed_nodes: ',spread_with_seed_nodes,' spread_with_seed_nodes_and_u: ',spread_with_seed_nodes_and_u)
    return ((spread_with_seed_nodes/n_iters), (spread_with_seed_nodes_and_u / n_iters))


# In[3]:


import heapq
class celf_node:
    def __init__(self, mg,flag):
        self.mg=mg
        self.flag=flag
    def __gt__(self, other):
        return self.mg> other.mg

def algo(graph, k, probability, iteration=1000):
    start_time = time.time()
    seed_set=[]
    queue=[]
    total_spread=0
    for u in (range(graph.vcount())):
        x,y=independent_cascade_model(graph, [], probability, iteration,u)
        mg=y-x
        flag=0
        heapq.heappush(queue,(-mg,u,celf_node(mg,flag))) 
    while len(seed_set)<k:
        sp,vertex_number,u=heapq.heappop(queue)
        if u.flag==len(seed_set):
            seed_set=seed_set+[vertex_number]
        else:
            x,y=independent_cascade_model(graph, seed_set, probability,iteration,vertex_number)#-independent_cascade_model(graph, seed_set, probability, iteration)
            u.mg=y-x
            u.flag=len(seed_set)
            heapq.heappush(queue,(-u.mg,vertex_number,u))
            total_spread=y
    end_time=time.time()
    #spread=independent_cascade_model(graph, seed_set, probability, iteration,)
    x,y=independent_cascade_model(graph, seed_set, probability,iteration,vertex_number)#-independent_cascade_model(graph, seed_set, probability, iteration)
           
    return seed_set,round(y*100/graph.vcount(),2), round(end_time-start_time, 2)


