Ant Hill Optimization
=====================

Srijan Sehgal
-------------

Ant hill optimization for network routing.

It is an algorithm based on the behaviour of the real ants in finding a shortest path from a source to the food.

This algorithm utilizes the behaviour of the real ants while searching for the food. It has been observed that the ants deposit a certain amount of pheromone in its path while traveling from its nest to the food. Again while returning, the ants are subjected to follow the same path marked by the pheromone deposit and again deposit the pheromone in its path. In this way the ants following the shorter path are expected to return earlier and hence increase the amount of pheromone deposit in its path at a faster rate than the ants following a longer path.

ACO takes the inspiration from the foraging behaviour of the ants. These ants deposit pheromone on the ground in order to mark some favourable path that should be followed by other members of the colony. However, the pheromone is subjected to evaporation by a certain amount at a constant rate after a certain interval and therefore the paths visited by the ants frequently, are only kept as marked by the pheromone deposit, whereas the paths rarely visited by the ants are lost because of the lack of phreromone deposit on that path and as a result the new ants are intended to follow the frequently used paths only. Thus, all the ants starting their journey can learn from the information left by the previously visitor ants and are guided to follow the shorter path directed by the pheromone deposit.

In ACO, a number of artificial ants(here data packets) build solutions to the considered optimization problem at hand and exchange information on the quality of these solutions via a communication scheme that is pheromone deposit on the path of the journey performed by it.
