# CPRs-

common_pool_uncertainty model is designed to study the impact of  different uncertainty levels regarding the resource size and  social interaction, i.e flow of information among fishermen located within a given radius on the harvesting behaviour of a group of fishermen exploiting a common pool resource that spatially varies. The model is developed for decision makers on the management  of renewable natural resource to help advance the design of policies geared towards sustaining the resources.

The model has two agents, namely fishermen  and fish agent which lives in a two dimensional world. The fishermen are characterized by their effort and catch. Every agent has a position (x and y coordinates) and changes this position by a random amounts in discrete time. The two-dimensional world is wrapped to keep the movement of the fishermen and fishes within a fixed boundary.  The model runs on a yearly time scale for a 250th years or stops if all the fishes get depleted earlier before this time-step.

The fishermen are characterized by their total catch, which is determined by the fishing effort exerted. When a fisherman agent has many other fishermen agents in its surrounding radius, the accuracy of its perception regarding the number of fishes increases. There is a random difference between the true and perceived number of fishes. The perceived number of fishes of the fishermen is a random number from a Gaussian distribution with a mean of the true number of fishes and a standard deviation  which represents the extent to which perception of the number of fishes of all the fishermen as a whole can deviate from the true number of fishes. 

The fish reproduction rate is density dependent and according to a logistic growth rate restriction. The fishermen moves by setting the heading towards the direction of any fish they sight (there is an equal probability of sighting or not sighting a fish) and moving a fixed-magnitude forward. If no fish is sighted, then the fisherman set a random-heading and moves fixed-magnitude forward. The fish moves in a random-walk by setting heading to a random angle and moving a fixed-magnitude  forward. The newly reproduced fishes starts its life at the location of its parents but however diffuses with  with time as they make random movements. The movement of both the fishermen and fishes occurs within torus landscape (i.e.when agents approach a border of the landscape, they re-enter the system at the opposite border).



