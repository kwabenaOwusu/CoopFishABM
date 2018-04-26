# Agent-based model (ABM) for marine protected areas (MPAs)

## Information
The model code is implemented in python. It generates an output folder named **simulation_output** in your working directory  which contains a video of the simulation (**simulation_video.mp4**), data of the catch and biomass dynamics of the fishermen (**simulation_data.csv**)  and snapshots of each time step of the simulation . 

## **Purpose**
Our agent-based model (ABM) focus on simulating  interaction between fisherman and the Eastern Central Atlantic fishery (western and central Africa). We seek to investigate how the size, age and spatial designs of marine protected areas (MPA), otherwise known as no-take zones or marine reserves affects the harvesting behaviour of the artisanal fishermen. The specific questions this model addresses are: (1) Which spatial design of MPA provides greatest protection to biomass and catch to fishermen. (2) What is the impact of size, age and the cooperation levels on the conservation effects of MPA?. 



## Usage ##
(1) For a no MPA simulation for entire period : \
MPA = 'no'   \
Both = 'no' 

(2) For a single MPA simulation for entire period : \
MPA = 'yes'    \
Both = 'no'  \
Type_MPA = 'single' \
Frac_MPA = [0,1] 

(3) For a spaced MPA simulation for entire period : \
MPA = 'yes'     \
Both = 'no'  \
Type_MPA = 'spaced' \
Dist_MPA = [0,1]  \
Frac_MPA = [0,1] 

(4) For partly no MPA and partly single MPA simulation for entire period : \
MPA = 'no'    \
Both = 'yes'  \
Time_MPA = ( ,total number of years of simulation] \
Type_MPA = 'single' \
Dist_MPA = [0,1] \
Frac_MPA = [0,1] 

(5) For partly no MPA and partly spaced MPA simulation : \
MPA = 'no'  
Both = 'yes'  
Time_MPA = ( ,total number of years of simulation]\
Type_MPA = 'spaced' \
Dist_MPA = [0,1] \
Frac_MPA = [0,1] 






