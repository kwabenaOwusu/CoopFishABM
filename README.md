# Agent-based model (ABM) for marine protected areas (MPAs)

## Information
The model code is implemented in python. It generates an output folder named *simulation_output* in your working directory  which contains a video of the simulation (*simulation_video.mp4*), data of the catch and biomass dynamics of the fishermen (*simulation_data*.csv)  and snapshots of each time step of the simulation . 

## **Purpose**
Our agent-based model (ABM) focus on simulating  interaction between fisherman and the Eastern Central Atlantic fishery (western and central Africa). We seek to investigate how the size, age and spatial designs of marine protected areas (MPA), otherwise known as no-take zones or marine reserves affects the harvesting behaviour of the artisanal fishermen. The specific questions this model addresses are: (1) Which spatial design of MPA provides greatest protection to biomass and catch to fishermen. (2) What is the impact of size, age and the cooperation levels on the conservation effects of MPA?. 



# Type of simulation
(1) For a no MPA simulation for entire period :
MPA = 'no'   # run simulation with an MPA? 
Both = 'no'  # run simulation partly without MPA and partly with MPA? 

(2) For a single MPA simulation for entire period :
MPA = 'yes'   # run simulation with an MPA?
Both = 'no'  # run simulation partly without MPA and partly with MPA? 
Type_MPA = 'single' # If MPA  = 'yes' or Both = 'yes', which type of MPA? : spaced or single
Frac_MPA = [0,1]  # What fraction of the total fishing area should be covered by MPA ? 

(3) For a spaced MPA simulation for entire period :
MPA = 'yes'   # run simulation with an MPA?
Both = 'no'  # run simulation partly without MPA and partly with MPA? 
Type_MPA = 'spaced' # If MPA  = 'yes' or Both = 'yes', which type of MPA? 
Dist_MPA = [0,1] # If Type_MPA = 'spaced', What should be the distance between MPA ?
Frac_MPA = [0,1]  # What fraction of the total fishing area should be covered by MPA ? 

(3) For partly no MPA and partly single MPA simulation for entire period :
MPA = 'no'   # run simulation with an MPA? 
Both = 'yes'  # run simulation partly without MPA and partly with MPA? : no or yes
Time_MPA = (,number of years for simulation] # If Both = 'yes', which time to introduce the MPA? 
Type_MPA = 'single' # If MPA  = 'yes' or Both = 'yes', which type of MPA? : spaced or single
Dist_MPA = [0,1] # If Type_MPA = 'spaced', What should be the distance between MPA ?
Frac_MPA = [0,1] # What fraction of the total fishing area should be covered by MPA ? 

(3) For partly no MPA and partly spaced MPA simulation :
MPA = 'no'   # run simulation with an MPA? : no or yes (where a 'yes' implies only with MPA and 'no' implies run only without MPA)
Both = 'yes'  # run simulation partly without MPA and partly with MPA? : no or yes
Time_MPA = 20 # If Both = 'yes', which time to introduce the MPA? 
Type_MPA = 'single' # If MPA  = 'yes' or Both = 'yes', which type of MPA? : spaced or single
Dist_MPA = 0.3 # If Type_MPA = 'spaced', What should be the distance between MPA ?
Frac_MPA = 0.15  # What fraction of the total fishing area should be covered by MPA ? 



Our agent-based model (ABM) simulates the interaction between two agents namely, fisherman and the fish on a finite two-dimensional world. We seek to investigate how different marine protected areas (MPAs) spatial designs, otherwise known as no-take zones or marine reserves affects the harvesting behaviour of artisanal fishermen under different levels of cooperation. We considered four levels of marine protected area spatial design namely, (1) **NO** (2) **SINGLE LARGE** (3) **CLOSELY SPACED** and (4) **DISTANTLY SPACED**. The total surface area covered by the different MPA spatial design are equal. We also considered three levels of cooperation namely, (1) **LOW** : more noncooperator relatively to cooperator fishermen (2) **INTERMEDIATE** : equal number of cooperator and noncooperator fishermen and (3) **HIGH** : more cooperator relativelly to noncooperator fishermen. The number of fishermen in the different cooperation level is equal.  The specific questions our model addresses are: (1) Which  MPA spatial design provides greatest protection to fish biomass and highest fish catch to fishermen. (2) What is the impact of different levels of cooperation on the conservation effects of the different MPA spatial design?#



