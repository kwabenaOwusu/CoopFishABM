# common_pool_uncertainty model

## Usage
The model code is implemented in python. To run the model, you need to place **pycxsimulator.py** in the same directory where **common_pool_uncertainty.py** is located.

## **Overview**

### Purpose

We develop an agent-based model to study the impact of different uncertainty levels regarding the resource size as well as social interaction, i.e. number of other agents located within a neighbourhood radius, on the harvesting behaviour of a group of fishermen exploiting a common pool resource. The model is developed for decision makers on management of renewable natural resource to help advance the design of resource management interventions.

### Entities, state-variables and scales

The model has two agents, namely a fisherman and fish agent which lives in a two dimensional world. Every agent has a position (x and y coordinates) and changes this position by a random amount in discrete time. The movement on the two-dimensional world occurs within torus landscape (i.e. when agents approach a border of the landscape, they re-enter the system at the opposite border). A fishermen can only harvest fish in a neighbourhood radius (<span class="math">_r_</span>) centred at it. Each step in the model represents a year and we run the simulations for 250 years or until all the fishes get depleted, whatever occurs first. The model code is implemented in python.

### Process overview and scheduling

Fishermen form a perception of the number of fishes. There is a random difference between the true and perceived number of fishes. We explicitly modeled this difference as a Gaussian probability distribution a mean of the true number of fishes (<span class="math">_N_<sub>_f_</sub></span>) and a standard deviation (<span class="math">_U_<sub>_f_</sub></span>), which represents the extent to which perception of the number of fishes of all the fishermen as a whole can deviate from the true number of fishes. The harvesting behaviour of a fisherman is determined by its harvesting coefficient, which is quantified as the absolute difference between its perceptions of the number of fishes from the true number of fishes. The harvesting coefficient also decreases by a constant factor for each other fisherman located in a fisherman’s neighbourhood radius. Hence, a higher number of other fishermen in neighborhood radius result in a lower harvesting coefficient. 

To determine whether to harvest, a random number is drawn from the uniform distribution and if it is less-than harvesting coefficient, a fish in neighbourhood radius is harvested. This is executed once for each fish agent in the neighbourhood radius. Thus, with a high harvesting coefficient and low number of other fishermen, a fisherman is more probable to harvest a larger fraction of the fishes in its neighborhood radius. The fishermen moves by setting the heading towards the direction of any fish they sight (there is an equal probability of sighting or not sighting a fish) and moving a fixed-magnitude (<span class="math">_M_<sub>_F_</sub></span>) forward. If no fish is sighted, then the fisherman set a random-heading and moves fixed-magnitude forward.

The fish agent growth rate is according to a logistic growth rate restriction. A copy of a randomly selected fish agent is created as an offspring if logistic growth rate restriction is not satisfied. The fish moves in a random-walk by setting heading to a random angle and moving a fixed-magnitude (<span class="math">_M_<sub>_f_</sub></span>) forward. The newly reproduced fish starts its life at the location of its parent but however diffuses with time as they make random movements.


