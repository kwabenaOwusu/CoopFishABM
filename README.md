# Agent-based model (ABM) for marine protected areas (MPAs)

## Information
The model code is implemented in python. It generates an output folder named **simulation_output** in your working directory  which contains a video of the simulation (**simulation_video.mp4**), data of the catch and biomass dynamics of the fishermen (**simulation_data.csv**)  and snapshots of each time step of the simulation . 

## **Purpose**
Our agent-based model (ABM) focus on simulating  interaction between fishermen and the Senegalese fishery. The fishing unit (i.e. fishermen on the same pirogue) and biomass are initially distributed randomly on a finite two-dimensional world. The biomass can decline or increase over time but the number of fishermen remains finite. We seek to examine the effects of the size, age (time elapsed since the establishment) and spatial designs (single, closely or distantly spaced) of marine protected areas (MPA), otherwise known as no-take zones or marine reserves on the harvesting behaviour of the artisanal fishermen. The specific questions we addresse with our model are: (1) Whether MPA can serve as a possible insurance policy to sustain marine ecosystems?  (2) What is the impact of the spatial design, size and age of MPA on its conservation effects at different cooperation levels?. 

## Usage ##
(1) For a no MPA simulation for entire period : \
MPA = 'no'   \
Both = 'no' 

(2) For a single MPA or spaced MPA simulation for entire period : \
MPA = 'yes'    \
Both = 'no'  \
Type_MPA = 'single' or 'spaced'\
Frac_MPA = [0,1] \
Dist_MPA = [0,1] (if 'spaced')  

(3) For partly no MPA and partly single MPA simulation or partly spaced MPA simulation : \
MPA = 'no'    \
Both = 'yes'  \
Time_MPA = ( ,total number of years of simulation (i.e MPA age)] \
Type_MPA = 'single' or 'spaced' \
Frac_MPA = [0,1] \
Dist_MPA = [0,1] (if 'spaced')







