# Effects of cooperation and different characteristics of Marine Protected Areas on a simulated artisanal fishery

## NOTE 
The model code is implemented in python. It generates an output folder named **simulation_output** in your working directory  which contains a video of the simulation (**simulation_video.mp4**), data of the catch and biomass dynamics of the fishermen (**simulation_data.csv**)  and snapshots of each time step of the simulation . 

## WHAT IS IT ?
We present here an Agent-Based Model (ABM) that captures, in broad terms, the main characteristics of a small-scale, artisanal fishery. We then use the model to disentangle the combined effects of fishing behaviour, expressed by a cooperative trait associated to fishing effort, and different designs of no-take fishery areas, including presence or absence, size, distance, and age, on fish abundances and catches.

There are two agent types, the fishing agents (i.e. pirogues with fishing crews, marked with circles) and fishes (marked with triangles) are initially randomly distributed on a finite 2-D space. The different colors of the fishing units reflect the associated cooperative trait level, ranging from fully cooperative (black) to fully non-cooperative (lightest gray). 

The reproduction of fish agents is simulated as a stochastic process depending on a reproduction probability and on a logistic-type growth restriction. The fish agent movement is simulated using three sensory zones around the fish, namely, repulsion zone, parallel-orientation zone, and attraction zone. The harvest rate of a fishing agent is described according to Schaefer’s model. The fishing agent moving towards the direction of a neighbouring agent exhibiting a greatest catch.

## HOW TO USE IT

MPA = 'yes'  # run with-only-MPA simulation? (A 'yes' implies only-with-MPA and 'no' implies only-without-MPA)
Both = 'no'  # run partly without-MPA and with-MPA? (A 'yes' implies partly (with-MPA and  with-MPA))
Time_MPA = 50 # If Both = 'yes', which time do you want to terminate the MPA? 
Type_MPA = 'spaced' # If MPA  = 'yes' or Both = 'yes', which spatial configuration do you want? (A 'spaced' implies two MPAs and 'single' implies only one MPA)
Dist_MPA = 0.2 # If Type_MPA = 'spaced', What should be the distance between the two MPAs ?
Frac_MPA = 0.25  # What fraction of the fishing environments should be set as MPA?
