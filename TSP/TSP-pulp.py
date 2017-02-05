# this first line only to keep plot in line with this notebook

import matplotlib.pyplot as plt
plt.style.use("ggplot") # plot style - more beautiful charts
import numpy as np
import pandas as pd
import pulp as plp

# Matrix of distances
# Matrix of distances
dist = np.array([[0,     2,     999999,12, 5     ],
                 [2,     0,     4,     8,  999999],
                 [999999,4,     0,     3,  3     ],
                 [12,    8,     3,     0,  10    ],
                 [5,     999999,3,     10, 0     ]])


# Distance from city B to D
dist[1][3]

cities = list(range(5))                 

# Create pulp problem
prob = plp.LpProblem("TSP", plp.LpMinimize)

# Decision variable X_i_j = 1 if we go from city i to j
X = plp.LpVariable.dicts("X", (cities,cities), 0, 1, plp.LpBinary)


# Objective function
prob += plp.lpSum([dist[i][j]*X[i][j] for i in cities for j in cities])


# constraints
for i in cities:
    prob += plp.lpSum([X[i][j] for j in cities]) == 1
    
for j in cities:
    prob += plp.lpSum([X[i][j] for i in cities]) == 1
    
    
prob.solve()