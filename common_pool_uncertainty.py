# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import random as rd
import math
import copy as cp
import numpy as np
from random import gauss 
import csv
import  matplotlib.pyplot as plt
from itertools import izip

## standard (nominal or reference) parameters for initialising the model ##

k = 100 # carrying capacity 
reg_prob =  0.03 # reproduction probability of the fishes
init_res = 20 # initial number of fishes
num_fishers = 30 # number of fishermen
r = 0.1 # neighbourhood radius of the fisherman 
r_sqr = r ** 2 # radius squared
move_res = 0.1 # magnitude of movement of fishes
move_fishers = 0.2 # magnitude of movement of fishermen 
res_uncert = 0.4  # extent to which perception regarding the number of fishes of the group of fishermen as a whole can deviate from 
#the true number of  fishes (0.4,0.8,1.2) N.B: Maximum uncertainty allowed is 1.2 (WHY? will be explained later)


class agent:  
    pass

def initialize():
    ''' 
    We study the impact of different uncertainty levels regarding the resource size as well as 
    social interaction, i.e. number of other agents located within a neighborhood radius, on the 
    harvesting behaviour of a group of fishermen exploiting a common pool resource. The model is
    developed for decision makers on management of renewable natural resource to help advance the 
    design of resource management interventions.
    
    '''
    global agents, res_data, hav_data, hav1_data, time
    time = 0.
    agents = []
    res_data = [init_res]  # number of fishes level initialised @ time zero bcos simulation starts at time 1
    hav_data = [0]  # total-harvest ...
    hav1_data = [0]  # total-current-harvest ...
    
    
   # Intialising agent-types, harvest and spatial-location
    for i in xrange(num_fishers + init_res ):    
        ag = agent()
        ag.type = 'fishers' if i < num_fishers else 'res'  # agent-type
        if ag.type == 'fishers':
            ag.harvest = 0 # initialise fishermen harvest
            ag.effort = 0 # initialise fishermen effort (harvesting coefficient)
            
        else:
            pass
            
        ag.x = math.cos(2*math.pi*rd.random()) # randomly take 0 =< angle =< 2 pi  and generate an x-coordinate in range -1 =< ag.x =< 1 
        ag.y = math.sin(2*math.pi*rd.random()) # randomly take  0 =< angle =< 2 pi  and generate an y-coordinate in range -1 =< ag.x =< 1    
        agents.append(ag)
        
   
def observe():                                    
    global agents, res_data, hav_data, hav1_data, time
    
    subplot(2, 2, 1)
    cla()
    resource = [ag for ag in agents if ag.type == 'res']
    if len(resource) > 0:
        x0 = [ag.x for ag in resource]
        y0 = [ag.y for ag in resource]
        plot(x0, y0, 'go')  
    fishermen = [ag for ag in agents if ag.type == 'fishers']
    if len(fishermen) > 0:
        x1 = [ag.x for ag in fishermen]
        y1 = [ag.y for ag in fishermen]
        plot(x1, y1, 'ro')
    axis('image')
    axis([-1,1,-1 ,1])
    plt.title('time step =' + str(int(time)))
     
    subplot(2, 2, 2)
    cla()
    plot(hav1_data, label = 'current harvest',color = 'b')
    #plt.xlabel('time', fontsize = 16)
    plt.ylabel('current harvest', fontsize=16)
    plt.title('mean harvest =' +  str(round((sum(hav1_data) / float(num_fishers)),3)))
    legend()
    
    subplot(2,2,(3,6))
    cla()
    plot(res_data, label = 'fishes',color = 'g')
    plt.xlabel('time', fontsize = 16)
    plt.ylabel('fishes', fontsize=16)
    plt.title('mean fishes level =' +  str(round(mean(res_data),3)))
    legend()
     
    

def update():
    global agents, res_data, hav_data, hav1_data, time
    time += 1. / len(agents) 
    #if int(time) == 150: # a time-step is reached. #if sum(1 for x in agents if x.type == 'res') == 0:  #stop if all fishes is depleted
         #return
    ag = agents[randint(len(agents))]    #randomly selected agents (can be fishes or fisherman)
        
        
# The fishes moves in random-walk by turning random angles and moving a fixed-magnitude forward.The random-walk of fishes
# agent is to occur  within torus landscape (i.e.when agents approach a border of the landscape, they reenter the system at the 
# opposite border).     
    if ag.type == 'res': 
        theta_1 = 2*math.pi*rd.random()            # 0 =< angle =< 2 pi
        ag.x += move_res*math.cos(theta_1)         # -1 =< ag.x =< 1  / added to previous cordinate / moves m_res forward
        ag.y += move_res*math.sin(theta_1)                 
        ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x  
        ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
        
        
# Fishes reproduce according to a density dependent and logistic growth rate restriction. 
        if rd.uniform(0, 1) < reg_prob * (1-sum(1 for x in agents if x.type == 'res')/float(k)):  # logistic growth
            agents.append(cp.copy(ag))  # creates a copy of the agents     
       
    
    else: # if a fisherman
        neighbors1 = [nb for nb in agents if nb.type == 'res' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] #fishes in neighborhood
        neighbors2 = [nb for nb in agents if nb.type == 'fishers' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr and nb != ag] #other-fishermen in neighborhood
        num_res = (sum(1 for x in agents if x.type == 'res')) # total number of fishes
        
        guess_res = rd.gauss(num_res, res_uncert) # perception of fishes level
        res_dev = abs(num_res - guess_res) # deviation of guessestimated fishes from the actual number of fishes,i.e. harvesting coefficient
        ag.effort =  (res_dev / 3.6)  #  scaling; since min(res_dev) = 0 and max(res_dev) = 3(1.2); normalized = (x-min(x))/(max(x)-min(x))
        ag.effort = 1 if ag.effort > 1 else ag.effort  # but 99.7% will be the case.
        
        for i in neighbors1:
                if rd.uniform(0, 1) < (ag.effort - (0.005 * len(neighbors2))):  # effort and interaction with fishermen in neighborhood affects harvesting behaviour
                    agents.remove(i)   # harvest fishes                         
                    ag.harvest += 1  # update number of fishes harvested         
                    
        neighbors3 = [nb for nb in agents if nb.type == 'res' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] #fishes in neighborhood after harvest
        if len(neighbors3) > 0: # when fishes still available in neighborhood
            if rd.uniform(0, 1) <  0.5:  #  when fish is sighted
                rand_items = rd.sample([x for x in agents if x.type == 'res'], 1) # randomly sample one fish
                deltax = rand_items[0].x - ag.x ; deltay =  rand_items[0].y - ag.y # move in the direction of the fish
                theta_2 = math.atan2(deltay,deltax)
                ag.x += move_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1 and moves m_fishers forward
                ag.y += move_fishers*math.sin(theta_2)                 # -1 =< ag.y=< 1 and moves m_fishers forward
                ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
            else:
                theta_3 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                ag.x += move_fishers*math.cos(theta_3)                # -1 =< ag.x =< 1
                ag.y += move_fishers*math.sin(theta_3)                 # -1 =< ag.x =< 1
                ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
        else:
            theta_4 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
            ag.x += move_fishers*math.cos(theta_4)                # -1 =< ag.x =< 1
            ag.y += move_fishers*math.sin(theta_4)                 # -1 =< ag.x =< 1
            ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
            ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
                
                    
def carrying_capacity (val = k): # parameter setter tab

 '''
 maximum level of resource that can be sustained.
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global k
 k = int(val)
 return val

          
def regeneration_prob (val = reg_prob): # parameter setter tab

 '''
 probability of resource growth
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global reg_prob
 reg_prob = float(val)
 return val
 


def initial_fishes (val = init_res): # parameter setter tab
 '''
 initial resource level
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global init_res
 init_res = int(val)
 return val
 
 
def number_fishermen (val = num_fishers): # parameter setter tab
 '''
 number of fishermen.
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global num_fishers
 num_fishers = int(val)
 return val
 
 
def neighbourhood_radius (val = r): # parameter setter tab
 '''
 neighbourhood radius within which harvesting is possible.
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global r
 r = float(val)
 return val
 

def magnitude_fishes_movement (val = move_res ): # parameter setter tab
 '''
 magnitude of resource movement 
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global move_res
 move_res = float(val)
 return val
 

def magnitude_fishermen_movement (val = move_fishers ): # parameter setter tab
 '''
 magnitude of movement of fishermen 
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global move_fishers
 move_fishers = float(val)
 return val
 
 
 
def degree__of_uncertainty (val =  res_uncert ): # parameter setter tab
 '''
 level of uncertainty regarding the resource level
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global  res_uncert
 res_uncert = float(val)
 return val 
 
 

 
def update_one_unit_time():
    global agents, res_data, hav_data, hav1_data, time
    t = 0.
    if int(time)  == 250:
            return
    while t < 1. and len(agents) > 0:   
        t += 1. / len(agents)  # we assume a 1/n unit time passes by at each time, bcos of continous changing in number of agents. 
        update()               # thus on-average each agent execute the update function once at a time.
    
    
    res_data.append(sum(1 for x in agents if x.type == 'res'))   # total number of fishes
    hav_data.append(sum([ag.harvest for ag in agents if ag.type == 'fishers']))  # total harvest 
    hav1_data.append(hav_data[-1] - hav_data[-2])  #  current harvest at a time.
   
    csvfile = "Total_Current_Harvest.csv"   # a csv-file which produces the time-series of fishes and current harvest
    with open(csvfile, "wb") as output:
        writer = csv.writer(output) 
        writer.writerow(['resource','harvest'])
        writer.writerows(izip(res_data, hav1_data))
        

    

   
import pycxsimulator
pycxsimulator.GUI(parameterSetters = [carrying_capacity, regeneration_prob,initial_fishes, number_fishermen, neighbourhood_radius, 
magnitude_fishermen_movement, magnitude_fishes_movement, degree__of_uncertainty]).start(func=[initialize, observe, update_one_unit_time])




             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
          


    
   


