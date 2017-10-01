# CPRs-
\subsection*{\bf Overview}

 \subsubsection*{Purpose}
We develop an agent-based model to study the impact of  different uncertainty levels regarding the resource size and  social interaction, i.e flow of information among fishermen located within a given radius on the harvesting behaviour of a group of fishermen exploiting a common pool resource that spatially varies. The model is developed for decision makers on the management  of renewable natural resource to help advance the design of policies geared towards sustaining the resources.

\subsubsection*{Entities, state-variables and scales}
The model has two agents, namely fishermen  and fish agent which lives in a two dimensional world. The fishermen are characterized by their effort and catch. Every agent has a position (x and y coordinates) and changes this position by a random amounts in discrete time. The two-dimensional world is wrapped to keep the movement of the fishermen and fishes within a fixed boundary.  The model runs on a yearly time scale for a 250th years or stops if all the fishes get depleted earlier before this time-step.

\subsubsection*{Process overview and scheduling}
The following actions are executed once per time in this given order: Fishermen forms a perception about the number of fishes. There is a random difference between the true and perceived number of fishes. The perceived number of fishes of the fishermen is a random number from a Gaussian distribution with a mean of the true number of fishes ($N_{f}$) and a standard deviation ($U_{f}$) which represents the extent to which perception of the number of fishes of all the fishermen as a whole can deviate from the true number of fishes. The effort ($E$) is quantified as the difference between a fisherman's perception of the number of fishes from the true number of fishes. The effort is also influenced by the number of  other-fishermen in the surrounding radius of a fisherman. The effort is scaled to  restricts the range from 0 to 1.  A fishermen can only harvest fish in its surrounding radius ($r$) centered at it. Harvesting a fish requires that 

\medskip
 
\begin{minipage}{0.9\textwidth}\raggedright
 \begin{equation}
 \mbox{ random-uniform (0,1)}  <  (E - \alpha \ast n_{f}) \label{eq3}
 \end{equation}

where $E$ is the effort of the fisherman, $ n_{f}$ is the number of fishermen in surrounding radius, $\alpha$ is a factor of reduction in effort for a fisherman within the surrounding radius and $\mbox{ random-uniform (0,1)} $ is a uniform distribution of evenly distributed values over a specified range (minimum value of 0 and a maximum of 1).
\end{minipage}

\bigskip
 
\noindent 
In other words, a random number is drawn from the uniform distribution and if it is less-than the expression at the right-hand-side (R.H.S) of \ref{eq3}, harvesting is successful. For example, if the R.H.S has a  value of (say 0.1), then in 10 \% of the cases, a random number drawn from the uniform distribution will be less-than the R.H.S  and harvesting condition will be true, for the other 80 \% cases the condition will be false. The procedure \ref{eq3} is executed for all fishes available in the surrounding radius of a fisherman. Thus if right-hand-side (R.H.S) of \ref{eq3} is very high, i.e high effort ($E$) and lower number of other fishermen ($n_{f}$), the probability is high that most or all fishes in surrounding radius will be harvested, however if the effort is low and there are more other fishermen, then very few of the fishes in the surrounding radius will be harvested.

 
\medskip

\noindent 
The fish reproduction rate is density dependent and according to a logistic growth rate restriction. A fish agent reproduce another fish agent  if:

 \medskip
 
\begin{minipage}{0.9\textwidth}\raggedright
 \begin{equation}
 \mbox{ random-uniform (0,1)}  <  R \left(1- \frac{N_{f}}{K}\right) \label{eq4}
 \end{equation}

where $R$ is the reproduction probability of the fishes probability, $N_{f}$ is the number fishes and $K$ is the carrying capacity. Reproduction stops  when $N_{f}$ equals $K$ and high values of $R$ increases the reproduction rate of the fishes. 
\end{minipage}

 \bigskip

\noindent

The fishermen moves by setting the heading towards the direction of any fish they sight (there is an equal probability of sighting or not sighting a fish) and moving a fixed-magnitude ($M_{F}$) forward. If no fish is sighted, then the fisherman set a random-heading and moves fixed-magnitude forward. The fish moves in a random-walk by setting heading to a random angle and moving a fixed-magnitude ($M_{f}$) forward. The newly reproduced fishes starts its life at the location of its parents but however diffuses with  with time as they make random movements. The movement of both the fishermen and fishes occurs within torus landscape (i.e.when agents approach a border of the landscape, they re-enter the system at the opposite border). 
