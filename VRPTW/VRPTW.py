#!/usr/bin/env python
# -- coding: utf-8 --

'''
VRPTW - Vehicle Routing Problem with Time Windows



'''

from __future__ import (absolute_import, division, print_function,
    generators, nested_scopes, unicode_literals, with_statement)

# ===================================================================
#     Python code to solve Vehicle Routing Problem with Time Windows
#     For this project we used Gurobi® for academic purposes  

#  Author: Rennan Danilo Seimetz Chagas
#  email: chagasrennan@gmail.com
# ===================================================================


from gurobipy import *

with open("./solomon_25/C102.txt", 'r') as f:
    lines = f.readlines()

instname = lines[0]

ncli = map(int,lines[4].split())[0]
cap = map(int,lines[4].split())[1]

rgcli = range(1, ncli+1)
cli = list(range(1, ncli+1))      # list of clients
nodes = list(range(ncli+2))       # list of clients
veh = list(rgcli)               # list of vehicles

# clients coordinates
xycli = {i:map(int,(lines[9+i].split()[1],lines[9+i].split()[2])) for i in nodes[:-1]}
xycli[nodes[-1]] = xycli[0]

# demands per clients
demand = map(int,[lines[9+i].split()[3] for i in nodes[:-1]])
demand.append(demand[0])

# release date time window
rd = map(int,[lines[9+i].split()[4] for i in nodes[:-1]])
rd.append(0)

# due date time window
dd = map(int,[lines[9+i].split()[5] for i in nodes[:-1]])
dd.append(float('inf'))

# service time
sv = map(int,[lines[9+i].split()[6] for i in nodes[:-1]])
sv.append(sv[0])

# costs ci,j
c = [[((xycli[i][0]-xycli[j][0])**2 + (xycli[i][1]-xycli[j][1])**2)**0.5 for i in nodes] for j in nodes]
# c.append(c[0])
print
bigM = 9999
lbigm = [[c[i][j] + dd[i] - rd[j] for i in nodes[:-1]] for j in nodes[:-1]]
# print(lbigm)

# create model 
m = Model('vrptw')

# create variable Xi,j,k
# 1, if vehicle k drives directly from vertex i to vertex j 
x = m.addVars(nodes, nodes, veh, 
                name='x',
                vtype=GRB.BINARY) 

# variable si,k
# the time vehicle k starts to service customer i.
s = m.addVars(nodes, veh, 
                name='s',
                vtype=GRB.CONTINUOUS)

# Objetctive Function
m.setObjective(
    quicksum(x[i,j,k]*c[i][j] for i in nodes for j in nodes for k in veh if i!=j),
    # obj,
    GRB.MINIMIZE
)

# Constraints
m.addConstrs(
    # each customer is visited exactly once
    (quicksum(x[i,j,k] for j in nodes for k in veh if j!=i) == 1 for i in cli) 
)  

m.addConstrs(
    # a vehicle can only be loaded up to it's capacity
    (quicksum(x[i,j,k]*demand[i] for i in cli for j in nodes if i!=j) <= cap for k in veh)
)

m.addConstrs(
    # each vehicle must leave the depot 0
    (quicksum(x[0,j,k] for j in nodes) == 1 for k in veh)
)

m.addConstrs(
    # after a vehicle arrives at a customer it has to leave for another destination
    (quicksum(x[i,h,k] - x[h,j,k] for i in nodes for j in nodes if i!=j) == 0 for h in cli for k in veh)
)

m.addConstrs(
    # all vehicles must arrive at the depot n + 1. The inequalities
    (quicksum(x[i,nodes[-1],k] for i in nodes if i!= nodes[-1]) == 1 for k in veh)
)

m.addConstrs(
    # the relationship between the vehicle depar- ture time from a customer and its immediate successor
    (s[i,k] + c[i][j] - bigM*(1 - x[i,j,k]) - s[j,k] <= 0 for i in nodes for j in nodes for k in veh)
)

m.addConstrs(
    # time windows are observed
    (rd[i] - s[i,k] <= 0 for i in nodes[:-1] for k in veh)
)

m.addConstrs(
    # time windows are observed
    (s[i,k] - dd[i] <= 0 for i in nodes[:-1] for k in veh)
)

# Solve
m.optimize()

m.write('vrptw.lp')

print('Objetivo: ', m.objVal)

for i in nodes:
    for j in nodes:
        for k in veh:
            if x[i,j,k].x > 0.001:
                print('x[',i,',',j,',',k,']=', x[i,j,k])