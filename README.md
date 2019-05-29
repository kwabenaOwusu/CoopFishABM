# Effects of cooperation and different characteristics of Marine Protected Areas on a simulated artisanal fishery

> ## NOTE
The **CoopFishABM.py** contains the model code and is the main script to run. It is implemented in python. It will generate an output folder named **simulation_output** in your working directory  which contains a video of the simulation (**simulation_video.mp4**), data of the catch and fish abundance dynamics of the fishing agent (**simulation_data.csv**) and snapshots of each computing time step of the simulation . 

> ## WHAT IS IT ?
We present here an Agent-Based Model (ABM) that captures, in broad terms, the main characteristics of a small-scale, artisanal fishery. We then use the model to disentangle the combined effects of fishing behaviour, expressed by a cooperative trait associated to fishing effort, and different designs of no-take fishery areas, including presence or absence, size, distance, and age, on fish abundances and catches.

There are two agent types, the fishing agents (i.e. pirogues with fishing crews, marked with circles) and fishes (marked with triangles) are initially randomly distributed on a finite 2-D space. The different colors of the fishing units reflect the associated cooperative trait level, ranging from fully cooperative (black) to fully non-cooperative (lightest gray). 

The reproduction of fish agents is simulated as a stochastic process depending on a reproduction probability and on a logistic-type growth restriction. The fish agent movement is simulated using three sensory zones around the fish, namely, repulsion zone, parallel-orientation zone, and attraction zone. The harvest rate of a fishing agent is described according to Schaefer’s model. The fishing agent moving towards the direction of a neighbouring agent exhibiting a greatest catch.

> ##  HOW TO USE IT

* The **MPA** sets whether to run an MPA or without an MPA throughout the entire period.
* The  **Both** sets whether to run partly with MPA and partly without an MPA simulation.
* The  **Time_MPA** determines which time to terminate MPA, if **Both** is set to "yes".
* The **Type_MPA** determines the spatial configuration required (i.e. "spaced" or "single"), If **MPA**  = 'yes' or **Both** = 'yes'.
* The **Dist_MPA** sets the distance between the two MPAs, if **Type_MPA** = "spaced".
* The **Frac_MPA** sets the fraction of the fishing ground to be set as MPA, IF **MPA** = "yes" or **Both** = "yes"

> ##  THINGS TO NOTICE

* How does a simulation with-MPA of a given configuration (size, age, or/ and distance between two MPAs) compares with same simulation without-MPA  in terms of fish abundance and catch?
* Does the speed of fish agent have any impacts on the conservation effects of an MPA of a specific configuration (size, age, or/ and distance between two MPAs) ?
* Does the different cooperation levels (regulation of catchability) affects the conservation effects of an MPA of a specific configuration (size, age, or/ and distance between two MPAs) ?

> ##  EXTENDING THE MODEL 

* In this model, we do not include life-history traits of the fish agents. Try extending the model by implementation of multiple fish species with different behavioural attributes and life-history traits.
* Complexity can be also added to fishing agents to investigate in more detail cooperative self-governance, which can be achieved with a variety of mechanisms, including monitoring, sanctioning, and reciprocity. 






