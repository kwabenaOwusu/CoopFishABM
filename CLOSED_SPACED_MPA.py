# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# An agent-based model to investigate harvesting behaviour of artisanal fishermen
# under a CLOSED-SPACED  marine protected area (MPA) consisting of fishermen of 
# different cooperative-trait distribution.
# By : OWUSU, Kwabena Afriyie
# Date : 24th February, 2018
#----------------------------------------------------------------------------

# create a subfolder to keep all plot-files and data
import shutil, os
subdir = 'CLOSED_SPACED_MPA' # subfolder name for plot files
if os.path.isdir(subdir): # does the subfolder already exist?
    shutil.rmtree(subdir) # delete the whole folder
os.mkdir(subdir) # make new subfolder
os.chdir(subdir) # move to subfolder
#---------------------------------------------------------------------------

# Importing the relevent library
from pylab import *
import copy as cp
import random as rd
import math
import numpy as np
import  matplotlib.pyplot as plt
import csv # write-out data output
from statistics import mean
#---------------------------------------------------------------------------------------------------

# Parameters
K = 150 # carrying capacity of fishing environment 
growth_prob =  0.1 # growth probability of a fish 
init_fish = 100 # initial number of a fish 
move_fish = 0.1 # magnitude of movement of a fish 
rad_repulsion = 0.05 # radius of repulsion zone
rad_orientation = 0.1 # radius of orientation zone
rad_attraction = 0.15 # radius of attraction zone

rad_repulsion_sqr = rad_repulsion ** 2
rad_orientation_sqr = rad_orientation ** 2
rad_attraction_sqr = rad_attraction ** 2

num_fishers = 20 # number of fishermen
move_fishers = 0.25 # magnitude of movement of a fisherman 
q = 0.7 # catch per unit effort (catchability)
r = 0.15 # neighbourhood radius of a fisherman (NB: the movement of fisherman shd be greater than the radius  )
r_sqr = r ** 2 # radius squared

# Distribution of cooperative-trait (sum up to number of fishermen (num_fishers))#
fully_noncoop = 4 # number of fully_noncooperative fishermen
noncoop = 4 # number of non_cooperative fishermen
cond_coop = 4 # number of conditional_cooperative fishermen
coop = 4 # number of cooperative fishermen
fully_coop = 4 # number of fully_cooperative fishermen

n = 300 # time-period for a simulation
#-------------------------------------------------------------------------------------------------------

class agent:  # create an empty class
    pass     
    
#----------------------------------------------------------------------------------------------------------    

def initialize():
    ''' 
     An agent-based model to investigate harvesting behaviour of heterogenous artisanal fishermen under a CLOSED-SPACED
     marine protected area (MPA) .
    '''
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2    
    time1 = 0. # time
    agents = []  # empty list to contain all agents
    fish_data = [init_fish]  # list to contain number of fish agents
    total_hav_data = {} # empty dictionary to contain total harvest based on cooperative-trait of all fishermen 
    current_hav_data  = {} # empty dictionary to contain current harvest based on cooperative-trait of all fishermen
    fishermen_data1 = [0] # list to contain total harvest of fishermen agents
    fishermen_data2 = [0] # list to contain current harvest of fishermen agents
    
    # Attributes of agents  (fishers and fish)
    for j in range(num_fishers + init_fish):    
        ag = agent()
        ag.type = 'fishers' if j < num_fishers else 'fish'  # set first ith_num_fishers as fishermen and remaining as fish
        if ag.type == 'fishers':
            ag.harvest = 0 # initialise harvest as zero for all fishermen
            if j < (fully_noncoop): # set first ith_fully_noncoop fishermen-agents as fully_noncooperators
                ag.effort = 1.0    # predefined effort corresponding to fully_noncooperators
                ag.trait = 'fully_noncoop' # set their cooperative-trait
                ag.num = 'fully_noncoop%d'% (1 + j) # to set fully_noncooperators as "fully_noncooperators1, fully_noncooperators2, etc." 
               
            elif (fully_noncoop) <= j < (fully_noncoop + noncoop): # set second ith_noncoop fishermen-agents as noncooperators
                ag.effort = 0.8
                ag.trait = 'noncoop'
                ag.num = 'noncoop%d'% ((1 + j) - fully_noncoop) 
                
            elif (fully_noncoop + noncoop) <= j < (fully_noncoop + noncoop + cond_coop ): # set third ith_cond_coop fishermen-agents as conditiornal cooperators
                ag.effort = 0.6
                ag.trait = 'cond_coop'
                ag.num = 'cond_coop%d'% ((1 + j) - (fully_noncoop + noncoop)) 
                
            elif (fully_noncoop + noncoop + cond_coop ) <= j < (fully_noncoop + noncoop + cond_coop + coop ): # set fourth ith_coop fishermen-agents as cooperators
                ag.effort = 0.4
                ag.trait = 'coop'
                ag.num = 'coop%d'% (1 + j - (fully_noncoop + noncoop + cond_coop)) 
                 
            elif (fully_noncoop + noncoop + cond_coop + coop ) <= j < (fully_noncoop + noncoop + cond_coop + coop + fully_coop): # # set fifth ith_fully_coop fishermen-agents as fully_cooperators
                ag.effort = 0.2
                ag.trait = 'fully_coop'
                ag.num = 'fully_coop%d'% (1 + j - (fully_noncoop + noncoop + cond_coop + coop))
            
            total_hav_data[ag.num]  = [ag.harvest]  # initialise total_harvest of different fishermen_trait
            current_hav_data [ag.num]  = [ag.harvest] # initialise current_harvest of different fishermen_trait
                
            while True: # randomly assign spatial_position to fishermen 
                ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
                ag.y = math.sin(2*math.pi*rd.random()) # sin of an angle  in [0 , 2pi] radian 
                if all([not((-0.6 <= ag.x <= -0.2) and (-0.4 <= ag.y <= 0.4)), 
                        not((0.2 <= ag.x <= 0.6) and (-0.4 <= ag.y <= 0.4))]): # keep looping until spatial_position falls outside the MPA
                    break
                # ALTERNATIVELLY : if ((ag.x <= x1 or ag.x >= x2) and ag.y >= -1) or ((x1 <= ag.x <= x2) and ag.y<= y1 or ag.y>= y2):
                
        else: # if a fish
            ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
            ag.y = math.sin(2*math.pi*rd.random()) # sin of an angle  in [0 , 2pi] radian 
          
        agents.append(ag) # put all agents into the list called agents
     
    fish_data_MPA = [sum([1 for j in agents if j.type == 'fish' and 
    any([((-0.6 <= j.x <= -0.2) and (-0.4 <= j.y <= 0.4)), ((0.2 <= j.x <= 0.6) and (-0.4 <= j.y <= 0.4))])])]
        

#------------------------------------------------------------------------------------------------------------------        
        
def observe():
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2    
   
    cla() # clear
    fishermen = [ag for ag in agents if ag.type == 'fishers']  # fisherman-agents
    if len(fishermen) > 0:
        X_fully_noncoop = [ag.x for ag in fishermen if ag.trait == 'fully_noncoop'] # x-axis
        Y_fully_noncoop = [ag.y for ag in fishermen if ag.trait == 'fully_noncoop'] # y-axis
        X_noncoop = [ag.x for ag in fishermen if ag.trait == 'noncoop']
        Y_noncoop = [ag.y for ag in fishermen if ag.trait == 'noncoop']
        X_cond_coop = [ag.x for ag in fishermen if ag.trait == 'cond_coop']
        Y_cond_coop = [ag.y for ag in fishermen if ag.trait == 'cond_coop']
        X_coop = [ag.x for ag in fishermen if ag.trait == 'coop']
        Y_coop = [ag.y for ag in fishermen if ag.trait == 'coop']
        X_fully_coop = [ag.x for ag in fishermen if ag.trait == 'fully_coop']
        Y_fully_coop  = [ag.y for ag in fishermen if ag.trait == 'fully_coop']
        
        # set five different color of reds using cmap 
        colors = np.r_[np.linspace(0.1, 1, 5), np.linspace(0.1, 1, 5)] 
        mymap = plt.get_cmap("Reds") ; my_colors = mymap(colors) 
         
        # plot fisherman-agents
        plt.plot(X_fully_noncoop, Y_fully_noncoop, 'o', color = my_colors[4], markersize=9, label='fully_noncoop')
        plt.plot(X_noncoop, Y_noncoop,  'o', color = my_colors[3], markersize=9, label='noncoop')
        plt.plot(X_cond_coop, Y_cond_coop, 'o', color = my_colors[2], markersize=9, label='conditional_coop')
        plt.plot(X_coop, Y_coop, 'o', color = my_colors[1], markersize=9, label='coop')
        plt.plot(X_fully_coop, Y_fully_coop, 'o', color = my_colors[0], markersize=9, label='fully_coop')
        
    fish = [ag for ag in agents if ag.type == 'fish']  #  fish-agents
    if len(fish) > 0:
        X_fish = [ag.x for ag in fish]
        Y_fish = [ag.y for ag in fish]
        plt.plot(X_fish, Y_fish, 'g^', markersize=3, label='fish') #  plot  fish-agents
        
    axis('image') ; axis([-1,1,-1 ,1]) ; plt.grid(False) ; plt.xticks([], []) ; plt.yticks([], [])  # plt.axis('off') axis , grid and axis-ticks
    #plt.title('Time-step ='+ str(int(time1))) # title
    #plt.legend(numpoints=1, loc= 'center', bbox_to_anchor=(0.5, -0.072), ncol=3, prop={'size':11}) # legend, prop to shrink its size
   
   # Lines enclosing the MPA
    plt.vlines(-0.6, -0.4, 0.4,lw=2, color='k') # (x1,y1,y2) 
    plt.vlines(-0.2, -0.4, 0.4, lw=2, color='k') # (x2,y1,y2)
    plt.hlines(-0.4,-0.6, -0.2, lw=2, color='k') # (y1,x1,x2)
    plt.hlines(0.4, -0.6, -0.2, lw=2, color='k') # (y2, x1,x2)
    
    plt.vlines(0.2, -0.4, 0.4,lw=2, color='k') # (x1,y1,y2) 
    plt.vlines(0.6, -0.4, 0.4, lw=2, color='k') # (x2,y1,y2)
    plt.hlines(-0.4,0.2, 0.6 ,lw=2, color='k') # (y1,x1,x2)
    plt.hlines(0.4, 0.2, 0.6, lw=2, color='k') # (y2, x1,x2)
    
    plt.savefig('abm_%04d.png' % time1, bbox_inches='tight', pad_inches=0 ) # save-figures to frames folder , dpi=200
    #plt.show()
    
    
#------------------------------------------------------------------------------------------------------------------

def update_fish():
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2    
    
    fish_ag = rd.sample([j for j in agents if j.type == 'fish'],1)[-1]     #randomly select an fish agent
    
    repulsion = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_repulsion_sqr] # fishes within the repulsion zone
    alignment = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_repulsion_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_orientation_sqr ] # fishes within the orientation zone
    attraction =[nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_orientation_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_attraction_sqr ] # fishes within the attraction zone
    
    if len(repulsion) > 0: # if fishes within repulsion zone, move away from the spot that would be the center of mass (midpoint) of all  fish within repulsion zone
        repulsion_x = mean([j.x for j in repulsion])
        repulsion_y = mean([j.y for j in repulsion])
        repulsion_1 = (math.atan2((repulsion_y - fish_ag.y), (repulsion_x - fish_ag.x)) + math.pi ) % (2 * math.pi) # if greater than  (2 * math.pi)
        theta = repulsion_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step    
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) > 0]):   # if fishes within orientation zone, change heading to match the average heading of all the other fish  within orientation zone     
        alignment_1 = mean([math.atan2((j.y - fish_ag.y),(j.x - fish_ag.x)) for j in alignment])
        theta = alignment_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step   
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) > 0]): # if fishes within the attraction zone, head towards the middle (midpoint) of the fish in zone of attraction.   
        attraction_x = mean([j.x for j in attraction ])
        attraction_y = mean([j.y for j in attraction])
        attraction_1 = math.atan2((attraction_y - fish_ag.y), (attraction_x - fish_ag.x))
        theta = attraction_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step      
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) == 0]): # if no fishes in all the zone, move random direction  
        theta = 2*math.pi*rd.random()  
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step     
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
           
    if rd.random() < growth_prob * (1-sum([1 for j in agents if j.type == 'fish'])/float(K)):  # logistic growth of fishes
        agents.append(cp.copy(fish_ag)) # add-copy of fish agent  
       
#------------------------------------------------------------------------------------------------------------------                        
                  
def update_fisherman():
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2    
    
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1]    #randomly select an fisherman agent
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr 
        and  all([not((-0.6 <= nb.x <= -0.2) and (-0.4 <= nb.y <= 0.4)), not((0.2 <= nb.x <= 0.6) and (-0.4 <= nb.y <= 0.4))])] # detecting fishes in neighbourhood
        
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish to be harvested based on (q*E*x), where x is number of fishes in neighborhood 
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fishes in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove fishes harvested
        fisherman_ag.harvest += 1  # add to harvest of the fisherman
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type == 'fishers' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort agents in neighborhood accoding to harvest
    if all([len(fishers_neighbors_harvest) > 0 , fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest]) : # if there exist fisherman in neighbourhood 
        deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   #move in the direction of one with greater harvest iiff 
        deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
        theta_1 = math.atan2(deltay,deltax) 
        if all([not((-0.6 <= (fisherman_ag.x + move_fishers*math.cos(theta_1)) <= -0.2) and (-0.4 <= (fisherman_ag.y + move_fishers*math.sin(theta_1)) <= 0.4)), 
                not((0.2 <= (fisherman_ag.x + move_fishers*math.cos(theta_1) <= 0.6)) and (-0.4 <= (fisherman_ag.y + move_fishers*math.sin(theta_1)) <= 0.4))]):
                fisherman_ag.x +=  move_fishers*math.cos(theta_1) # move 'move_fishers' in the direction of neighbour fishermen with greater harvest 
                fisherman_ag.y +=  move_fishers*math.sin(theta_1) 
                fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y

          
        else:  # 
            theta_empt1 = 0 ; theta_empt2 = 0
            while True: # in the case it can land you on an MPA move in a random direction
                theta_2 = 2*math.pi*rd.random()
                fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
                fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
                theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
                if all([not((-0.6 <= fisherman_ag.x <= -0.2) and (-0.4 <= fisherman_ag.y <= 0.4)), 
                        not((0.2 <= fisherman_ag.x <= 0.6) and (-0.4 <= fisherman_ag.y <= 0.4))]):
                        fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                        fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                        break
    
    else:                    
       theta_empt1 = 0 ; theta_empt2 = 0
       while True: # in the case it can land you on an MPA move in a random directiontheta_3 = 2*math.pi*rd.random() 
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
            if all([not((-0.6 <= fisherman_ag.x <= -0.2) and (-0.4 <= fisherman_ag.y <= 0.4)), 
                    not((0.2 <= fisherman_ag.x <= 0.6) and (-0.4 <= fisherman_ag.y <= 0.4))]):
                    fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                    fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                    break
                    
#------------------------------------------------------------------------------------------------------------------                                

def update_one_unit_time():
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2    
    time1 += 1 
    
    t = 0.
    while t < 1. and sum([1 for j in agents if j.type == 'fish']) > 0:   
        t += 1. / len(fish)  # we assume a 1 / (number of fishes) time passes by per time. 
        update_fish()       # thus on-average each fish agent is updated once per time.
    
    t = 0.
    while t < 1. :   
        t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
        update_fisherman()        # thus on-average each fish agent is updated once per time.
        
        
    # data preparation output 
      
    fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and 
                        any([((-0.6 <= j.x <= -0.2) and (-0.4 <= j.y <= 0.4)), 
                            ((0.2 <= j.x <= 0.6) and (-0.4 <= j.y <= 0.4))])])) # detecting number of fishes in MPA
    fish_data.append(sum([1 for j in agents if j.type == 'fish']))   # total number of fishes
    all_fishers = [[j.num, j.harvest] for j in agents if j.type =='fishers'] # fishermen 
    for j in all_fishers:
        total_hav_data[j[0]].append(j[-1])  # append each fishermans total harvest  to dictionary 'total_hav_data' based on its cooperative-trait
        current_hav_data[j[0]].append(total_hav_data[j[0]][-1] - total_hav_data[j[0]][-2])  # append each fishermans current harvest  to dictionary 'current_hav_data'
    
    fishermen_data1.append(sum([j.harvest for j in agents if j.type == 'fishers']))   # total harvest of fishermen
    fishermen_data2.append(fishermen_data1[-1] - fishermen_data1[-2])   # current harvest of fishermen
    
    csvfile = "close_mpa.csv"   # a csv-file output 
    header = [key for key in sorted(current_hav_data)]
    header.append('total_haverst') ; header.append('total_fish') ; header.append('fish_MPA')
    main_data = [current_hav_data[key] for key in sorted(current_hav_data)]
    main_data.append(fishermen_data2) ; main_data.append(fish_data) ; main_data.append(fish_data_MPA)
    with open(csvfile, "w") as output:
        writer = csv.writer(output) 
        writer.writerow(header)
        writer.writerows(zip(*main_data))
        
#------------------------------------------------------------------------------------------------------------------        

# time-period for a simulation
initialize()
observe()

for j in range(1, n):
        update_one_unit_time()
        observe()
   
#------------------------------------------------------------------------------------------------------------------ 

os.chdir(os.pardir) # optional: move up to parent folder

#------------------------------------------------------------------------------------------------------------------ 










































             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
          


    
   


