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

k = 100 # carrying capacity of the fishes
reg_prob =  0.03 # reproduction rate of the fishes
init_res = 20 # initial number of fishes 
num_fishers = 30 # number of fishermen
r = 0.1 # radius of the neighborhood centered at a fishermen to guessestimate fishes
r_sqr = r ** 2 # radius squared
move_res = 0.1 # magnitude of movement of fishes
move_fishers = 0.2 # magnitude of movement of fishermen 
res_uncert = 0.4 # degree of uncertainty of guesestimated fishes (0,0.4,0.8,1.2) N.B: Maximum uncrtainty allowed is 1.2



class agent:  
    pass

def initialize():
    ''' 
    We explore the impact of different degree of uncertainties in perception of fishes (in neighbourhood)
    and the flow of information among fishermen on harvesting behaviour in a common pool fishery systems.
    
    '''
    global agents, res_data, hav_data, hav1_data,time
    time = 0.
    agents = []
    res_data = [init_res]  # initialised fishes level data  @ time 0 bcos simulation starts at time 1
    hav_data = [0] # initialised total-harvest data
    hav1_data = [0] # initialised total-current-harvest data 
    
    
   # Intialise the agent-types, harvest and location
    for i in xrange(num_fishers + init_res ):    
        ag = agent()
        ag.type = 'fishers' if i < num_fishers else 'res'  # agent-type
        if ag.type == 'fishers':
            ag.harvest = 0 # initialise fishermen harvest
            ag.effort = 0 # initialise fishermen effort
            #ag.dist = 'noncoop' if i < round(init_noncoop * num_fishers) else 'coop' # initial  number coop / noncoop 
            #ag.effort = rd.uniform((0.26*max_effort),max_effort) if ag.dist == 'noncoop' else rd.uniform(0,(0.25*max_effort))
            ## The fishermen considered as cooperators are assigned lower effort levels than those considered noncooperators.
        else:
            pass
            
        ag.x = cos(2*math.pi*rd.random()) # randomly take 0 =< angle =< 2 pi  and generate an x-coordinate in range -1 =< ag.x =< 1 
        ag.y = sin(2*math.pi*rd.random()) # randomly take  0 =< angle =< 2 pi  and generate an y-coordinate in range -1 =< ag.x =< 1    
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
        ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x  # magitude of movement helps to explain why it works.
        ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
        
        
# Fishes reproduce according to a density dependent and logistic growth rate restriction. 
        if rd.uniform(0, 1) < reg_prob * (1-sum(1 for x in agents if x.type == 'res')/float(k)):  # logistic growth
            agents.append(cp.copy(ag))  # creates a copy of the agents 
            
# Fishermen forms a perception about the number of fishes. There is a random difference between the true and perceived fishes level. 
# The difference is a gaussian distribution with a mean of true fishes level and a standard deviation (which quantifies the degree 
# of uncertainty in perceived fishes level). Fishermen vary their efforts (harvest-strategy) based on the level of uncertainties and 
# the number interactions they have with other fishermen in their neighborhood. Fishermen can only harvest fishes in a fixed-radius 
# neighborhood centered at them. Fishers who have more accurate information about the fishes and interact with many other fishermen
# harvest sustainably than those with less-accurate information about the fishes and interaction. Fishermen moves by setting the 
# heading towards nearest(distance) fishes in the neighborhood and moves a fixed-magnitude forward if they sight fishes in the 
# neighborhood(equal probability of sighting or not-sighting). If no fishes are available in the given neighborhood, or no fish
# is sighted,then it set a random-heading and moves fixed-magnitude forward.    
       
    
    else: # if a fisherman
        neighbors1 = [nb for nb in agents if nb.type == 'res' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] #fishes in neighborhood
        neighbors2 = [nb for nb in agents if nb.type == 'fishers' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr and nb != ag] #other-fishermen in neighborhood
        num_res = (sum(1 for x in agents if x.type == 'res')) # total number of fishes
        
        guess_res = rd.gauss(num_res, res_uncert) # perception of fishes level
        res_dev = abs(num_res - guess_res) # deviation of guessestimated fishes from the actual number of fishes
        ag.effort =  (res_dev / 3.6)  #  scaling; since min(res_dev) = 0 and max(res_dev) = 3(1.2);max allowed res-uncert is 1.2: 99.7% will be satisfied
        ag.effort = 1 if ag.effort > 1 else ag.effort
        
        for i in neighbors1:
                if rd.uniform(0, 1) < (ag.effort - (0.005 * len(neighbors2))):  # effort and interaction with fishermen in neighborhood
                    agents.remove(i)   # harvest fishes                         # affects harvesting behaviour
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
 probability of resource reproduction
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global reg_prob
 reg_prob = float(val)
 return val
 


def initial_fishes (val = init_res): # parameter setter tab
 '''
 initial resource.
 #initial_resource
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
 neighbourhood radius that can be harvested.
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
 magnitude of movement of fishermen if expectation is met
 Make sure you change this parameter while the simulation is not running,
 and reset the simulation before running it. Otherwise it causes an error!
 '''
 global move_fishers
 move_fishers = float(val)
 return val
 
 
 
def degree__of_uncertainty (val =  res_uncert ): # parameter setter tab
 '''
 level of uncertinty in resource level
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
        t += 1. / len(agents)  # we assume a 1/n unit time passes by at each time, bcos of continous changing number of agents. 
        update()               # thus on-average each agent execute the update function once at a time.
    
    
      
    res_data.append(sum(1 for x in agents if x.type == 'res'))   # total number of fishes
    hav_data.append(sum([ag.harvest for ag in agents if ag.type == 'fishers']))  # total number of fishermen
    hav1_data.append(hav_data[-1] - hav_data[-2])  #  current harvest at a time.
   
    
    
    csvfile = "/Users/kow/Desktop/W.csv"   # a csv-file which produces the time-series of fishes and current harvest
    with open(csvfile, "wb") as output:
        writer = csv.writer(output)
        writer.writerows(izip(res_data, hav1_data))
    
   
   
import pycxsimulator
pycxsimulator.GUI(parameterSetters = [carrying_capacity, regeneration_prob,initial_fishes, number_fishermen, neighbourhood_radius, 
magnitude_fishermen_movement, magnitude_fishes_movement, degree__of_uncertainty]).start(func=[initialize, observe, update_one_unit_time])




             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
          


    
   
















































            




  
      
"""
#(1 - (j / float(len(neighbors))))
# All fishermen set heading towards nearest(distance) resource from it for a fixed radius and moves fixed-magnitude forward. 
# If no resource is found within the given radius then the fishermen set a random-heading and moves fixed-magnitude forward.        
    
    for ag in agents:
        if ag.type == 'fishers':
            neighbors = [(math.sqrt((ag.x - nb.x)**2 + (ag.y - nb.y)**2),nb,ag,ag.discount) for nb in agents if nb.type == 'res' and
                (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < r_sqr ]
                 
            if len(neighbors) > 0:  # if a resource is within the fixed-radius
               rev_neighbors = sorted(neighbors,reverse = False)
               deltax = rev_neighbors[0][1].x - rev_neighbors[0][2].x ; deltay =  rev_neighbors[0][1].y - rev_neighbors[0][2].y
               theta_1 = math.atan2(deltay,deltax)
               ag.x += m_fishers*math.cos(theta_1)                # -1 =< ag.x =< 1 and moves m_fishers forward
               ag.y += m_fishers*math.sin(theta_1)                 # -1 =< ag.y=< 1 and moves m_fishers forward
               ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
               ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
            
           
               #The probability of harvesting depends on how close a resource is to a fisherman and the perception
               # of future resource productivity of that fisherman. For a given succesful harvest, cooperators increseases their 
               #perception of future productivity faster than non-cooperators. Similally for a given failure to harvest, non-cooperators
               # decreases perception of future productivity faster than non-cooperators.
              
               for i in rev_neighbors:
                   if rd.uniform(0, 1) > (i[0] + i[3]):  
                       agents.remove(i[1]) 
                       ag.harvest += 1 # cost of a unit resource
                       if ag.dist == 'cooperator':
                           ag.discount += 0.02
                           ag.discount = max_discount if ag.discount > max_discount else ag.discount
                       else:
                           ag.discount += 0.01
                           ag.discount = max_discount if ag.discount > max_discount else ag.discount
                            
                   else:
                       if ag.dist == 'cooperator':
                           ag.discount -= 0.01
                           ag.discount = 0 if ag.discount < 0 else ag.discount
                       else:
                           ag.discount -= 0.02
                           ag.discount = 0 if ag.discount < 0 else ag.discount
                    
   

                    
            
                    sort_neighbors = sorted(neighbors,reverse = False)
                    deltax = sort_neighbors[0][1].x - ag.x ; deltay =  sort_neighbors[0][1].y - ag.y
                    theta_1 = math.atan2(deltay,deltax)
                    ag.x += move_fishers*math.cos(theta_1)                # -1 =< ag.x =< 1 and moves m_fishers forward
                    ag.y += move_fishers*math.sin(theta_1)                 # -1 =< ag.y=< 1 and moves m_fishers forward
                    ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                    ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
                    j = 0
                    for i in sort_neighbors:
                        if rd.uniform(0, 1) > (ag.effort + i[0]):  
                            agents.remove(i[1]) 
                            ag.harvest += 1 
                            j += 1
                    if  j < guess_num_neighbors:
                        ag.effort = j / float(guess_num_neighbors)
                    elif j >= guess_num_neighbors :
                        ag.effort =  weight_effort 
                        
                else:
                    ag.effort =  0
                    
                     
                        
            else:   # perception of no resource is within the fixed-radius
                theta_2 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                ag.x += move_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1
                ag.y += move_fishers*math.sin(theta_2)                 # -1 =< ag.x =< 1
                ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
                
                
                
             
             #num_resource = sum(1 for x in agents if x.type == 'res')
            #other_agents = [nb for nb in agents if nb.type == 'fishers' and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < r_sqr and nb != ag]
            #guess_num_neighbors =  round(rd.gauss(num_neighbors, num_neighbors / 3)) ##np.random.normal(len(neighbors), 2,1)
            
            
            if len(neighbors) > 0:  # if a resource is within the fixed-radius
                sort_neighbors = sorted(neighbors,reverse = False)
                deltax = sort_neighbors[0][1].x - ag.x ; deltay =  sort_neighbors[0][1].y - ag.y
                theta_1 = math.atan2(deltay,deltax)
                ag.x += m_fishers*math.cos(theta_1)                # -1 =< ag.x =< 1 and moves m_fishers forward
                ag.y += m_fishers*math.sin(theta_1)                 # -1 =< ag.y=< 1 and moves m_fishers forward
                ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
                if guess_num_neighbors > 0:
                    j = 0
                    for i in neighbors:
                        if rd.uniform(0, 1) > (ag.discount + i[0]):  
                            agents.remove(i[1]) 
                            ag.harvest += 1 # cost of a unit resource
                            j += 1
                    if  j <= guess_num_neighbors:
                        ag.discount = j / float(guess_num_neighbors)
                        ag.discount = max_discount if ag.discount > max_discount else ag.discount
                    else :
                        ag.discount = max_discount
                    
                #j = 0  
                #for i in sort_neighbors:
                    #if rd.uniform(0, 1) > (ag.discount + i[0]):  
                        #agents.remove(i[1]) 
                        #ag.harvest += 1 # cost of a unit resource
                        #j += 1
                #ag.discount = j / float(len(neighbors))
                #ag.discount = max_discount if ag.discount > max_discount else ag.discount
                
            
                
            else:   # no resource is within the fixed-radius
                theta_2 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                ag.x += m_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1
                ag.y += m_fishers*math.sin(theta_2)                 # -1 =< ag.x =< 1
                ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
            
            
            
            if guess_num_neighbors > 0:
                j = 0  
                for i in neighbors:
                    if rd.uniform(0, 1) > (ag.discount + i[0]):  
                        agents.remove(i[1]) 
                        ag.harvest += 1 # cost of a unit resource
                        j += 1
                if  j <= guess_num_neighbors:
                    ag.discount = j / float(guess_num_neighbors)
                    ag.discount = max_discount if ag.discount > max_discount else ag.discount
                else :
                    ag.discount = max_discount
            
                 
              #The probability of harvesting depends on how close a resource is to a fisherman and the perception
               # of future resource productivity of that fisherman. For a given succesful harvest, cooperators increseases their 
               #perception of future productivity faster than non-cooperators. Similally for a given failure to harvest, non-cooperators
               # decreases perception of future productivity faster than non-cooperators.
              
            #if len(neighbors) > 0:
                #for i in sort_neighbors:
                    #if rd.uniform(0, 1) > (ag.discount + sort_neighbors[0][0]):  
                        #agents.remove(sort_neighbors[0][1]) 
                        #ag.harvest += 1 # cost of a unit resource
                        #ag.discount = float(len(neighbors)) / (len(neighbors) + len(other_agents))
                    #else:
                        #ag.discount = float(len(neighbors)) / (len(neighbors) + len(other_agents))
                        
           #for i in range(randint(len([ag for ag in agents if ag.type == 'res']) + 1)): # added plus one bcos randint(1) is zero.
        #if rd.uniform(0, 1) < reg_prob * (1-sum(1 for ag in agents if ag.type == 'res')/float(k)):
            #ag = agent()
            #ag.type = 'res' 
            #ag.x = cos(2*math.pi*rd.random())  
            #ag.y = sin(2*math.pi*rd.random())
            #agents.append(ag)
            #agents.append(cp.copy(ag))
            #if rd.uniform(0, 1) < reg_prob * (1-sum(1 for ag in agents if ag.type == 'res')/float(k)):
            #rand_items = random.sample(items, n) 
            
            
# A random sample of the resource generates a new resource units according to a density dependent and logistic growth rate. 
    
    #rand_res = (randint(sum(1 for x in agents if x.type == 'res') + 1)) # random number of resource and added plus one bcos randint(1) is zero.
    #rand_items = rd.sample([x for x in agents if x.type == 'res'], rand_res) # create a list of the random-nuber agents
    #for x in rand_items:
    #if rd.uniform(0, 1) < reg_prob * (1-sum(1 for x in agents if x.type == 'res')/float(k)):  # logistic growth
            #agents.append(cp.copy(ag))  # creates a copy of the agents                                            

                                                                     
                                                                                                                                          
                                                                                                                                                                                                               
if len(neighbors) > 0:  # if truly, a resource exist within the fixed neighborhood
                if guess_num_neighbors > 0:  # and perception is that resource exist within the fixed neighborhood
                    j = 0  
                    for i in neighbors:
                        if rd.uniform(0, 1) < (ag.effort - i[0]):   # a resource close to the agents is more likely to be harvested. 
                            agents.remove(i[1])   # remove agents
                            ag.harvest += 1  # update harvest
                            j += 1          # counter for harvest-success
                            
                    if  j < guess_num_neighbors:
                        ag.effort = (1 - (j / float(guess_num_neighbors)))
                        theta_2 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                        ag.x += move1_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1
                        ag.y += move1_fishers*math.sin(theta_2)                 # -1 =< ag.x =< 1
                        ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                        ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                        
                    elif j >= guess_num_neighbors :
                        ag.effort =  0.0
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
                    
                        
            else:
                if guess_num_neighbors > 0:
                    ag.effort =  max_effort
                    theta_5 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                    ag.x += move1_fishers*math.cos(theta_5)                # -1 =< ag.x =< 1
                    ag.y += move1_fishers*math.sin(theta_5)                 # -1 =< ag.x =< 1
                    ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                    ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                else:
                    theta_6 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
                    ag.x += move_fishers*math.cos(theta_6)                # -1 =< ag.x =< 1
                    ag.y += move_fishers*math.sin(theta_6)                 # -1 =< ag.x =< 1
                    ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                    ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y                                                                                                                                                                                                                                                                                                                                                         
    
           #guess_num_neighbors = round(rd.gauss(len(neighbors), res_knowledge)) # perception of resource for a given neighborhood
            #while (0 <= guess_num_neighbors <= k) == False:                     
                #guess_num_neighbors = round(rd.gauss(len(neighbors), res_knowledge ))

# A new resource is reproduced according to a density dependent and logistic growth rate restriction. This regeneration is also 
# dependent on predation by other factors other than human harvesting.

    rand_res = (randint(sum(1 for x in agents if x.type == 'res') + 1)) # random number of resource and added plus one bcos randint(1) is zero.
    rand_items = rd.sample([x for x in agents if x.type == 'res'], rand_res) # create a list of the random-nuber agents
    for x in rand_items:
        if rd.uniform(0, 1) < reg_prob * (1-sum(1 for x in agents if x.type == 'res')/float(k)): #- pred_prob:  # logistic growth
            agents.append(cp.copy(x))  # creates a copy of the agents  























else:
        neighbors = [(math.sqrt((ag.x - nb.x)**2 + (ag.y - nb.y)**2),nb) for nb in agents if nb.type == 'res' and
                ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] 
        other_agents = [nb for nb in agents if nb.type == 'fishers' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr and nb != ag]
        sort_neighbors = sorted(neighbors,reverse = False)
        sort_other_agents = sorted(other_agents,reverse = False)
        
        if len(neighbors) > 0 : 
            
            #deltax = sort_neighbors[0][1].x - ag.x ; deltay =  sort_neighbors[0][1].y - ag.y
            #theta_2 = math.atan2(deltay,deltax)
            #ag.x += move_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1 and moves m_fishers forward
            #ag.y += move_fishers*math.sin(theta_2)                 # -1 =< ag.y=< 1 and moves m_fishers forward
            #ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
            #ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y

            
            # generate the certainty of resource reproduction(from 0 to 1 interv)
            if ag.dist == 'coop':
                # Make the probability of a higher-certainty (than observed) 2x more likely
                prob1 = [1.0] * (int(len(inter_val) / 2.) + 1) + [2.0] * (int(len(inter_val) / 2.)) 
                # Normalising to 1.0
                prob1 /= np.sum(prob1)
                discount = round(np.random.choice(inter_val, 1, p=prob1)[0],2)
            else:
                prob2 = [2.0] * (int(len(inter_val) / 2.)) + [1.0] * (int(len(inter_val) / 2.) + 1)
                prob2 /= np.sum(prob2)
                discount = round(np.random.choice(inter_val, 1, p=prob2)[0], 2) 
                
            if rd.uniform(0,1) > discount  :# Decision to harvest or not
                j = 0  
                for i in neighbors:
                    if rd.uniform(0, 1) < (ag.effort - i[0]):   # a resource close to the agents is more likely to be harvested. 
                        agents.remove(i[1])   # remove agents
                        ag.harvest += 1  # update harvest
                        j += 1  #(1. / float(len(neighbors))) # counter for harvest-success scaled for comparison to observed
                if  j >= len(neighbors) : #discount
                    ag.effort =  ag.effort
                    ag.effort = max_effort if ag.effort > max_effort else ag.effort
                else:
                    if len(sort_other_agents) > 0 :
                        if sort_other_agents[0].harvest > ag.harvest:
                            ag.effort = sort_other_agents[0].effort  
                            #ag.effort = max_effort if ag.effort > max_effort else ag.effort
                        ag.effort =  ag.effort
                    ag.effort =  ag.effort
                        
                
                    
                    
        else:
            theta_3 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
            ag.x += move_fishers*math.cos(theta_3)                # -1 =< ag.x =< 1
            ag.y += move_fishers*math.sin(theta_3)                 # -1 =< ag.x =< 1
            ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
            ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y











else:
        neighbors1 = [(math.sqrt((ag.x - nb.x)**2 + (ag.y - nb.y)**2),nb) for nb in agents if nb.type == 'res' and
                ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] 
        sort_neighbors1 = sorted(neighbors1,reverse = False)
        if len(neighbors1) > 0 :
            deltax = sort_neighbors1[0][1].x - ag.x ; deltay =  sort_neighbors1[0][1].y - ag.y
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

        
       
        neighbors = [(math.sqrt((ag.x - nb.x)**2 + (ag.y - nb.y)**2),nb) for nb in agents if nb.type == 'res' and
                ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] 
        sort_neighbors = sorted(neighbors,reverse = False)
        other_agents = [(nb.harvest,nb) for nb in agents if nb.type == 'fishers' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr and nb != ag]
        sort_other_agents = sorted(other_agents,reverse = False)
        
        if len(neighbors) > 0 : 
            # future certainty of resource productivity (either 0: NO or 1 : YES)
            inter_val = np.arange(0,2,1)
            if ag.dist == 'coop':
                # Probability of a YES is equally likely like NO for cooperators
                prob1 = [1.0] * 1 + [1.0] * 1 
                # Normalising to 1.0
                prob1 /= np.sum(prob1)
                discount = round(np.random.choice(inter_val, 1, p=prob1)[0],2)
            else:
                # Probability of a NO 2x more likely than a YES for noncooperators
                prob2 = [2.0] * 1 + [1.0] *  1
                prob2 /= np.sum(prob2)
                discount = round(np.random.choice(inter_val, 1, p=prob2)[0], 2) 
                
            if discount <= 0 :# Decision to Harvest or Not
                j = 0  
                for i in neighbors:
                    if rd.uniform(0, 1) < (ag.effort - i[0]):   # a resource close to the agents is more likely to be harvested. 
                        agents.remove(i[1])   # remove agents
                        ag.harvest += 1  # update harvest
                        j += 1   # counter for harvest-success 
                if  j < len(neighbors) : #discount
                    if len(sort_other_agents) > 0 :
                        ag.effort = sort_other_agents[-1][1].effort if sort_other_agents[-1][1].harvest > ag.harvest else ag.effort
                            
 
 distributedNoncooperators are twice more likely to discount
# a lower future resource level(than the current level) relativelly to a higher future resource level. Cooperators are twice more 
# likely to discount a higher future resource level(than the current level) relativelly to a lower future resource level. As the
# discount-factor increases the decision to forego a harvest and allow the resource to reproduce  also increases(lies btn 0 and 1).
# Fishermen moves by setting the heading towards nearest(distance) resource in the neighborhood moving fixed-magnitude forward. 
# If no resource is available in the given neighborhood, then it set a random-heading and moves fixed-magnitude forward.    
# The probability of harvesting a resource in the neighbourhood depends on how close (distance) it is to the fisherman and the 
# magnetude of the effort. The fishermen update their effort based on catch and observed number of resource.If catch exceeds or equals 
# , fishermen mantains their effort (since it pays) for the next time step. If catch is less than the observed number of 
# resource,fishermen increases effort for the next time-step.                       
                                             

                                                                                         
                                                                                                                                                                                  
                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                    
    else:
        neighbors = [(math.sqrt((ag.x - nb.x)**2 + (ag.y - nb.y)**2),nb) for nb in agents if nb.type == 'res' and
                ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr] 
        sort_neighbors = sorted(neighbors,reverse = False)
        
        other_agents = [(nb.harvest,nb) for nb in agents if nb.type == 'fishers' and ((ag.x - nb.x)**2 + (ag.y - nb.y)**2) < r_sqr and nb != ag]
        sort_other_agents = sorted(other_agents,reverse = False)
       
        guess_num_neighbors = round(rd.gauss(len(neighbors), res_uncert)) # perception of resource for a given neighborhood
        while (0 <= guess_num_neighbors <= k) == False:
            guess_num_neighbors = round(rd.gauss(len(neighbors), res_uncert ))
        
        if guess_num_neighbors > 0 :
            j = 0  
            for i in neighbors:
                if rd.uniform(0, 1) < (ag.effort - i[0]):   # a resource close to the agents is more likely to be harvested. 
                    agents.remove(i[1])   # remove agents
                    ag.harvest += 1  # update harvest
                    j += 1   # counter for harvest-success 
            if j < guess_num_neighbors:
                ag.effort += ((guess_num_neighbors - j) / float(k)) # difference scaled btn 0 and 1
                ag.effort = max_effort if ag.effort > max_effort else ag.effort
            elif j > guess_num_neighbors:
                ag.effort -= ((j - guess_num_neighbors) / float(k))
                ag.effort = 0 if ag.effort < 0 else ag.effort
            else:
                ag.effort = ag.effort
               
        #if len(sort_other_agents) > 0:
            #if sort_other_agents[-1][0] > ag.harvest:
                #deltax = sort_other_agents[-1][1].x - ag.x ; deltay =  sort_other_agents[-1][1].y - ag.y
                #theta_2 = math.atan2(deltay,deltax)
                #ag.x += move_fishers*math.cos(theta_2)                # -1 =< ag.x =< 1 and moves m_fishers forward
                #ag.y += move_fishers*math.sin(theta_2)                 # -1 =< ag.y=< 1 and moves m_fishers forward
                #ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
                #ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
                
        
        theta_3 = 2*math.pi*rd.random()                     # 0 =< angle =< 2 pi
        ag.x += move_fishers*math.cos(theta_3)                # -1 =< ag.x =< 1
        ag.y += move_fishers*math.sin(theta_3)                 # -1 =< ag.x =< 1
        ag.x = (ag.x - 2) if ag.x > 1 else (ag.x + 2) if ag.x < -1 else ag.x
        ag.y = (ag.y - 2) if ag.y > 1 else (ag.y + 2) if ag.y < -1 else ag.y
       
   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
     f j < guess_num_neighbors:
                ((guess_num_neighbors - j) / float((guess_num_neighbors - j) + 1)) # difference scaled btn 0 and 1
            else:
                ag.effort = ag.effort
                
      # available in the given neighbourhood, he attempts to harvest it. The probability of harvesting a resource depends on how close 
# (distance) it is to the fisherman and the magnitude of the effort exerted. If catch equals the perceived resource level, the 
# fishermen keeps their effort for the next harvest opportunity (mantains harvest strategy: no need to change a winning strategy). 
# If catch is not-equal to the perceived resource level, fishermen vary their effort based on the difference between the perceived 
# and true resource level.They increase the effort levels if catch is less than the percieved resource level (exert more effort 
# for the next harvest opportunity) or decrease if catch is greater-than  the perceived resource level(exert more efort for the 
# next harvest opportunity).           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
"""              
   
 

    
  

 


