# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# An agent-based model (ABM) to investigate harvesting behaviour of artisanal fishermen
# under different marine protected area (MPA) spatial design at different cooperation levels.

# By : OWUSU, Kwabena Afriyie
# Date : 6th April, 2018

#----------------------------------------------------------------------------
## Create a subfolder to keep all plot-files and data ##
import shutil, os
subdir = 'simulation_output' # subfolder name for plot files
if os.path.isdir(subdir): # does the subfolder already exist?
    shutil.rmtree(subdir) # delete the whole folder
os.mkdir(subdir) # make new subfolder
os.chdir(subdir) # move to subfolder


#---------------------------------------------------------------------------
## Import relevent libraries ##
from pylab import *
import copy as cp
import random as rd
import math
import numpy as np
import  matplotlib.pyplot as plt
import csv 
from statistics import mean
#---------------------------------------------------------------------------------------------------
## Parameters ##

# Fishing system
K = 150 # carrying capacity of fishing system 
n = 100 # time-period for a simulation 

# Fish characteristics 
growth_prob =  0.06 # growth probability of fish 
init_fish = 100 # initial fish biomass 
move_fish = 0.1 # speed of fish movement  
rad_repulsion = 0.025 # radius of repulsion zone of a fish
rad_orientation = 0.05 # radius of orientation zone of a fish
rad_attraction = 0.1 # radius of attraction zone of a fish
rad_repulsion_sqr = rad_repulsion ** 2
rad_orientation_sqr = rad_orientation ** 2
rad_attraction_sqr = rad_attraction ** 2

# Fisherman characteristics
num_fishers = 20 # number of fishermen 
move_fishers = 0.25 # speed of fisherman movement 
q = 0.65 # catch per unit effort-catchability
r = 0.15 # neighbourhood radius of a fisherman (Note: the speed of fisherman must be greater than the radius ) # 0.15
r_sqr = r ** 2 # radius squared

# Cooperation level (must sum up to total number of fishermen)
fully_noncoop = 4 # number of fully_noncooperative fishermen
noncoop = 4 # number of noncooperative fishermen
cond_coop = 4 # number of conditional_cooperative fishermen
coop = 4 # number of cooperative fishermen
fully_coop = 4 # number of fully_cooperative fishermen

# Type of simulation
MPA = 'no'   # run simulation with an MPA? : no or yes (where a 'yes' implies only with MPA and 'no' implies run only without MPA)
Both = 'no'  # run simulation partly without MPA and partly with MPA? : no or yes
Time_MPA = 20 # If Both = 'yes', which time to introduce the MPA? 
Type_MPA = 'single' # If MPA  = 'yes' or Both = 'yes', which type of MPA? : spaced or single
Dist_MPA = 0.3 # If Type_MPA = 'spaced', What should be the distance between MPA ?
Frac_MPA = 0.15  # What fraction of the total fishing area should be covered by MPA ? 

#-------------------------------------------------------------------------------------------------
# Computing cordinates for MPA based on type of simulation required
Half_Length = (math.sqrt(Frac_MPA*4)) / 2 # compute half the length  of MPA

# Coordinates for a single MPA
Xa = - Half_Length 
Xb =   Half_Length 
Ya = - Half_Length 
Yb =   Half_Length

# Points for first part of spaced MPA
Xm = - Half_Length - (Dist_MPA / 2)
Xn = -(Dist_MPA / 2) 
Ym = - Half_Length 
Yn =   Half_Length 
# Points for second part of spaced MPA
Xp = (Dist_MPA / 2) 
Xq =  Half_Length + (Dist_MPA / 2)
Yp = -Half_Length 
Yq =  Half_Length 

#-------------------------------------------------------------------------------------------------------

class agent:  # create an empty class
    pass     
    
#----------------------------------------------------------------------------------------------------------    

def initialize():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3 
    time1 = 0. # time
    agents = []  # empty list to contain all (fish biomass and fishermen)
    fish_data = [init_fish]  # list to contain number of fish biomass
    total_hav_data = {} # empty dictionary to contain total catch of fishermen by  cooperative-trait 
    current_hav_data  = {} # empty dictionary to contain current catch of fishermen by cooperative-trait 
    fishermen_data1 = [0] # list to contain total catch of fishermen 
    fishermen_data2 = [0] # list to contain current catch of fishermen 
    
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
            
            total_hav_data[ag.num]  = [ag.harvest]  # initialise total catch of fishermen by coopertive trait
            current_hav_data [ag.num]  = [ag.harvest] # initialise current_catch of different fishermen_trait
                
            if any([(MPA == 'no' and Both == 'no'), (MPA == 'no' and Both == 'yes' and Type_MPA == 'single'), (MPA == 'no' and Both == 'yes'and Type_MPA == 'spaced')]) : # only no MPA, partly no MPA and partly single or spaced MPA
                # randomly assign spatial_position to fishermen 
                ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
                ag.y = math.sin(2*math.pi*rd.random()) # sine of an angle  in [0 , 2pi] radian 
            
            elif (MPA == 'yes' and Type_MPA == 'single' and Both == 'no'): # only single MPA
                while True: # randomly assign spatial_position to fishermen
                    ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
                    ag.y = math.sin(2*math.pi*rd.random()) # sin of an angle  in [0 , 2pi] radian 
                    if not((Xa <= ag.x <= Xb) and (Ya <= ag.y <= Yb)) : # keep looping until spatial_position falls outside the MPA
                        break
                        
            elif (MPA == 'yes' and Type_MPA == 'spaced' and Both == 'no'): # only spaced MPA
                while True: # randomly assign spatial_position to fishermen 
                    ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
                    ag.y = math.sin(2*math.pi*rd.random()) # sin of an angle  in [0 , 2pi] radian 
                    if all([not((Xm <= ag.x <= Xn) and (Ym <= ag.y <= Yn)), 
                        not((Xp <= ag.x <= Xq) and (Yp <= ag.y <= Yq))]): # keep looping until spatial_position falls outside the MPA
                            break
        else: # if a fish
            ag.x = math.cos(2*math.pi*rd.random()) # cosine of an angle in [0 , 2pi] radian; thus values between [-1,+1]
            ag.y = math.sin(2*math.pi*rd.random()) # sin of an angle  in [0 , 2pi] radian 
          
        agents.append(ag) # put all agents 
        
    # Initialise the number of fishes within MPA 
    if any([(MPA == 'no' and Both == 'no'), (MPA == 'no' and Both == 'yes' and Type_MPA == 'single'), (MPA == 'no' and Both == 'yes'and Type_MPA == 'spaced')]) :
        fish_data_MPA = [0] #  a zero because no mpa is initiated
    elif (MPA == 'yes' and Type_MPA == 'single' and Both == 'no'): 
        fish_data_MPA = [sum([1 for j in agents if j.type == 'fish' and  ((Xa <= j.x <= Xb) and (Ya <= j.y <= Yb))])]
    elif (MPA == 'yes' and Type_MPA == 'spaced' and Both == 'no'):
        fish_data_MPA = [sum([1 for j in agents if j.type == 'fish' and any([((Xm <= j.x <= Xn) and (Ym <= j.y <= Yn)), ((Xp <= j.x <= Xq) and (Yp <= j.y <= Yq))])])]
    
    fishermen_data3 = [fish_data[-1] - fish_data_MPA[-1]] # initialise fish biomass outside MPA
 #------------------------------------------------------------------------------------------------------------------        
        
def observe():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3    
    plt.clf()  # clear figure
    plt.subplot(111, facecolor='lightskyblue') # background color
    
    fishermen = [ag for ag in agents if ag.type == 'fishers']  # fisherman
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
        
        # Set five different color of reds  
        colors = np.r_[np.linspace(0.1, 1, 5), np.linspace(0.1, 1, 5)] 
        mymap = plt.get_cmap("Reds") ; my_colors = mymap(colors) 
         
        # plot fisherman-agents
        plt.plot(X_fully_noncoop, Y_fully_noncoop, 'o', color = my_colors[4], markersize=7.5, label='fully_noncoop')
        plt.plot(X_noncoop, Y_noncoop,  'o', color = my_colors[3], markersize=7.5, label='noncoop')
        plt.plot(X_cond_coop, Y_cond_coop, 'o', color = my_colors[2], markersize=7.5, label='conditional_coop')
        plt.plot(X_coop, Y_coop, 'o', color = my_colors[1], markersize=7.5, label='coop')
        plt.plot(X_fully_coop, Y_fully_coop, 'o', color = my_colors[0], markersize=7.5, label='fully_coop')
        
    fish = [ag for ag in agents if ag.type == 'fish']  #  fish-agents
    if len(fish) > 0:
        X_fish = [ag.x for ag in fish]
        Y_fish = [ag.y for ag in fish]
        plt.plot(X_fish, Y_fish, '^', color='darkgreen', markersize=3, label='fish') #  plot  fish-agents
        
    if any([(MPA == 'yes' and Type_MPA == 'single' and Both == 'no'), (MPA == 'no' and Both == 'yes' and Type_MPA =='single' and time1 >= Time_MPA)]):
        #Lines enclosing single MPA
        plt.vlines(Xa, Ya, Yb, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xb, Ya, Yb, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Ya, Xa, Xb, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yb, Xa, Xb, lw=2, color='k') # (y2, x1,x2)
        
    elif any([(MPA == 'yes' and Type_MPA == 'spaced' and Both == 'no'), (MPA == 'no' and Both == 'yes' and Type_MPA =='spaced' and time1 >= Time_MPA)]):
        # Lines enclosing the first spaced MPA
        plt.vlines(Xm, Ym, Yn, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xn, Ym, Yn, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Ym, Xm, Xn, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yn, Xm, Xn, lw=2, color='k') # (y2, x1,x2)
         # Lines enclosing the second spaced MPA
        plt.vlines(Xp, Yp, Yq, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xq, Yp, Yq, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Yp, Xp, Xq, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yq, Xp, Xq, lw=2, color='k') # (y2, x1,x2)
    
    axis('image') ; axis([-1,1,-1 ,1]) ; plt.grid(False) ; plt.xticks([], []) ; plt.yticks([], [])  # plt.axis('off') axis , grid and axis-ticks
    plt.title('year =' + str(int(time1))) # title
    plt.legend(numpoints=1, loc= 'center', bbox_to_anchor=(0.5, -0.072), ncol=3, prop={'size':11}, facecolor='lightskyblue') # legend, prop to shrink its size, , facecolor='lightskyblue'
    plt.savefig('year_%04d.png' % time1, bbox_inches='tight', pad_inches=0 ,dpi=200) # save-figures to frames folder , dpi=1000
    #plt.pause(0.00001)
    #plt.show()
    
#------------------------------------------------------------------------------------------------------------------

def update_fish():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3    
    fish_ag = rd.sample([j for j in agents if j.type == 'fish'],1)[-1] #randomly select a fish 
    
    repulsion = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_repulsion_sqr] # fish biomass within the repulsion zone
    alignment = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_repulsion_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_orientation_sqr ] # fish biomass within the parallel-orientation zone
    attraction =[nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_orientation_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_attraction_sqr ] # fish biomass within the attraction zone
    
    if len(repulsion) > 0: # if fish biomass within repulsion zone, move away from the spot that would be the center of mass (midpoint) of all  fish within repulsion zone
        repulsion_x = mean([j.x for j in repulsion])
        repulsion_y = mean([j.y for j in repulsion])
        repulsion_1 = (math.atan2((repulsion_y - fish_ag.y), (repulsion_x - fish_ag.x)) + math.pi ) % (2 * math.pi) # if greater than  (2 * math.pi) then compute with a minus
        theta = repulsion_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step    
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) > 0]):   # if fish biomass within parallel-orientation zone, change direction to match the average direction of all the other fish  within parallel-orientation zone     
        alignment_1 = mean([math.atan2((j.y - fish_ag.y),(j.x - fish_ag.x)) for j in alignment])
        theta = alignment_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step   
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) > 0]): # if fish biomass within only the attraction zone, head towards the middle (midpoint) of the fish biomass in zone of attraction.   
        attraction_x = mean([j.x for j in attraction ])
        attraction_y = mean([j.y for j in attraction])
        attraction_1 = math.atan2((attraction_y - fish_ag.y), (attraction_x - fish_ag.x))
        theta = attraction_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step      
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) == 0]): # if no fishes in all the zone, move in a random direction  
        theta = 2*math.pi*rd.random()  
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step     
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -1) if fish_ag.x > 1 else (fish_ag.x % 1) if fish_ag.x < -1 else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -1) if fish_ag.y > 1 else (fish_ag.y % 1) if fish_ag.y < -1 else fish_ag.y  # they re-enter the system at the opposite border )  
                                                   
    if rd.random() < growth_prob * (1-sum([1 for j in agents if j.type == 'fish'])/float(K)):  # logistic growth of fish biomass
        agents.append(cp.copy(fish_ag)) # add-copy of fish agent  
       
#------------------------------------------------------------------------------------------------------------------                        
                  
def no_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3 
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1] # randomly sample a fisherman 
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr ] # detecting fish biomass in neighbourhood
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish to be harvested based on (q*E*x), where x is number of fish biomass in neighborhood 
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fish biomass in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove catch  
        fisherman_ag.harvest += 1  # add to catch of a fisherman
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type == 'fishers' and nb != fisherman_ag and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    if len(fishers_neighbors_harvest) == 0: # if there exist no fisherman in neighbourhood
        theta_1 = 2*math.pi*rd.random()
        fisherman_ag.x +=  move_fishers*math.cos(theta_1) # move  'move_fishers' step in a random direction
        fisherman_ag.y +=  move_fishers*math.sin(theta_1) 
        fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
        fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest]) : # if there exist fisherman with greater catch than focal fisherman 
            deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   #move in the direction of one with greater catch than focal fisherman 
            deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
            theta_2 = math.atan2(deltay,deltax) 
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greatest catch
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
            fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
    else: # if there exist fisherman but with less or equal catch relativelly  to focal fisherman
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
            fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
   
#-----------------------------------------------------------------------------------------------------------------

def single_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3   
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1]   #randomly select a fisherman
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr 
        and not((Xa <= nb.x <= Xb) and (Ya <= nb.y <= Yb))] # detecting fish biomass in neighbourhood and outside MPA
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish catch based on (q*E*x), where x is fish biomass in neighborhood  and outside MPA
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fish biomass in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove fish catch
        fisherman_ag.harvest += 1  # add to catch of fisherman
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type =='fishers' and nb != fisherman_ag  and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    if len(fishers_neighbors_harvest) == 0 : # if there exist no fisherman in neighbourhood:
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_1 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_1) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_1) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_1) ; theta_empt2 = move_fishers*math.sin(theta_1)
            if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                break
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest])  : # if there exist a fisherman in neighbourhood with greatest catch than focal fisherman
        deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   #move in the direction of one with greatest catch
        deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
        theta_2 = math.atan2(deltay,deltax) 
        if not((Xa <= (fisherman_ag.x + move_fishers*math.cos(theta_2)) <= Xb) and (Ya <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yb)):  # if updating  movement does not fall in MPA
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greatest catch 
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
            fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
        else:  # in case moving in this direction lands you on an MPA, move in a random direction
            theta_empt1 = 0 ; theta_empt2 = 0
            while True: 
                theta_2 = 2*math.pi*rd.random()
                fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
                fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
                theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
                if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                    fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                    fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                    break
    else:  # if there exist a fisherman in neighbourhood but with less or equal catch relativelly to focal fisherman
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
            if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                break
                            
#------------------------------------------------------------------------------------------------------------------                                

def spaced_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3   
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1]    #randomly select an fisherman 
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr and  all([not((Xm <= nb.x <= Xn) and (Ym <= nb.y <= Yn)), not((Xp <= nb.x <= Xq) and (Yp <= nb.y <= Yq))])] # detecting fish biomass in neighbourhood
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish catch based on (q*E*x), where x is number of fishes in neighborhood 
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fish biomass in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove fish catch
        fisherman_ag.harvest += 1  # add to fish catch
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type == 'fishers' and nb != fisherman_ag and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    if len(fishers_neighbors_harvest) == 0 : # if there exist no fisherman in neighbourhood 
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_1 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_1) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_1) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_1) ; theta_empt2 = move_fishers*math.sin(theta_1)
            if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                    fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                    fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                    break
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest]) : # if there exist fisherman in neighbourhood with greatest catch than focal fisherman 
        deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   # move in the direction of one with greatest catch 
        deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
        theta_2 = math.atan2(deltay,deltax) 
        if all([not((Xm <= (fisherman_ag.x + move_fishers*math.cos(theta_2)) <= Xn) and (Ym <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yn)), not((Xp <= (fisherman_ag.x + move_fishers*math.cos(theta_2) <= Xq)) and (Yp <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yq))]):
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greater harvest 
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
            fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
        else:  # in the case it lands you on an MPA move in a random direction
            theta_empt1 = 0 ; theta_empt2 = 0
            while True: 
                theta_2 = 2*math.pi*rd.random()
                fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
                fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
                theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
                if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                    fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                    fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                    break
    else:  # if there exist fisherman in neighbourhood with less or equal catch relativelly to focal fisherman 
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
            if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                fisherman_ag.x = -1 if fisherman_ag.x > 1 else  1 if fisherman_ag.x < -1 else fisherman_ag.x
                fisherman_ag.y = -1 if fisherman_ag.y > 1 else  1 if fisherman_ag.y < -1 else fisherman_ag.y
                break
   
#------------------------------------------------------------------------------------------------------------------                                

def update_one_unit_time():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3  
    time1 += 1  # update time
    
    t = 0.
    while t < 1. and sum([1 for j in agents if j.type == 'fish']) > 0:
        t += 1. / len(fish)  # we assume a 1 / (number of fishes) time passes by per time. 
        update_fish()       # thus on-average each fish agent is updated once per time.
        
    if (MPA == 'no' and Both == 'no' ): # no MPA is required throughout entire simulation
        t = 0.
        while t < 1. :   
            t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
            no_mpa()        # thus on-average each fish agent is updated once per time.
        fish_data_MPA.append(0) # append a zero since no MPA is required
       
    
    elif (MPA == 'yes' and Both == 'no') : #  MPA is required throughout entire simulation
        if Type_MPA == 'single' :
            t = 0.
            while t < 1. :  
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                single_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and ((Xa <= j.x <= Xb) and (Ya <= j.y <= Yb))])) #  fish biomass in MPA
        elif Type_MPA == 'spaced' :
            t = 0.
            while t < 1. :   
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                spaced_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and any([((Xm <= j.x <= Xn) and (Ym <= j.y <= Yn)), ((Xp <= j.x <= Xq) and (Yp <= j.y <= Yq))])])) #  fish biomass in MPA

        
    elif (MPA == 'no' and Both == 'yes' and Type_MPA == 'single') :
        if time1 < Time_MPA :
            t = 0.
            while t < 1. :  
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                no_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(0) 
        else :
            t = 0.
            while t < 1. :   
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                single_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and ((Xa <= j.x <= Xb) and (Ya <= j.y <= Yb))])) 

    
    elif (MPA == 'no' and Both == 'yes' and Type_MPA == 'spaced') :
        if time1 < Time_MPA :
            t = 0.
            while t < 1. :  
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                no_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(0) 
        else :
            t = 0.
            while t < 1. :   
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                spaced_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and any([((Xm <= j.x <= Xn) and (Ym <= j.y <= Yn)), ((Xp <= j.x <= Xq) and (Yp <= j.y <= Yq))])])) 

        
    # Preparation of data
    fish_data.append(sum([1 for j in agents if j.type == 'fish']))   # total fish biomass
    all_fishers = [[j.num, j.harvest] for j in agents if j.type =='fishers'] # fishermen 
    for j in all_fishers:
        total_hav_data[j[0]].append(j[-1])  # append each fishermans total catch to dictionary 'total_hav_data' based on its cooperative-trait
        current_hav_data[j[0]].append(total_hav_data[j[0]][-1] - total_hav_data[j[0]][-2])  # append each fishermans current catch to dictionary 'current_hav_data'
    
    fishermen_data1.append(sum([j.harvest for j in agents if j.type == 'fishers']))   # total  catch 
    fishermen_data2.append(fishermen_data1[-1] - fishermen_data1[-2])   # current catch 
    fishermen_data3.append(fish_data[-1] - fish_data_MPA[-1]) # fish biomass outside MPA
   
    
    
    csvfile = "simulation_data.csv"   # a csv-file output 
    header = [key for key in sorted(current_hav_data)]
    header.append('total_catch') ; header.append('total_biomass') ; header.append('biomass_inside_MPA') ; header.append('biomass_outside_MPA')
    main_data = [current_hav_data[key] for key in sorted(current_hav_data)]
    main_data.append(fishermen_data2) ; main_data.append(fish_data) ; main_data.append(fish_data_MPA) ; main_data.append(fishermen_data3)
    with open(csvfile, "w") as output:
        writer = csv.writer(output) 
        writer.writerow(header)
        writer.writerows(zip(*main_data))
       
#------------------------------------------------------------------------------------------------------------------        
#if __name__ == "__main__":
# Time-period for a simulation

initialize()  
observe()
    
for j in range(1, n):  
    update_one_unit_time()
    observe()

os.system("ffmpeg -v quiet -r 5 -i year_%04d.png -vcodec mpeg4  -y -s:v 1920x1080 simulation_movie.mp4") # convert files to a movie

#------------------------------------------------------------------------------------------------------------------ 

os.chdir(os.pardir) # optional: move up to parent folder

#----------------------------------------------------------------------------------------------------------------