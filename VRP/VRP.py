#!/usr/bin/env python
# -- coding: utf-8 --

from __future__ import (absolute_import, division, print_function,
    generators, nested_scopes, unicode_literals, with_statement)

# ==================================================================
#     Python code to solve simple Vehicle Routing Problem
#     For this project we used Gurobi® for academic purposes  

#  Author: Rennan Danilo Seimetz Chagas
#  email: chagasrennan@gmail.com
# ==================================================================


from gurobipy import *

with open("./solomon_25/C101.txt", 'r') as f:
    lines = f.readlines()

instname = lines[0]

ncli = map(int,lines[4].split())[0]
cap = map(int,lines[4].split())[1]

rgcli = range(ncli+1)

cli = list(rgcli)       # list of clients
veh = list(rgcli)       # list of vehicles

# clients coordinates
xycli = {i:map(int,(lines[9+i].split()[1],lines[9+i].split()[2])) for i in rgcli}

# demands per clients
demand = map(int,[lines[9+i].split()[3] for i in rgcli])

# release date time window
rd = map(int,[lines[9+i].split()[4] for i in rgcli])

# due date time window
dd = map(int,[lines[9+i].split()[5] for i in rgcli])

# service time
sv = map(int,[lines[9+i].split()[6] for i in rgcli])

# costs ci,j
c = [ [((xycli[i][0]-xycli[j][0])**2 + (xycli[i][1]-xycli[j][1])**2)**0.5 for i in rgcli] for j in rgcli]

# create model 
m = Model('vrptw')

# create variable Xi,j,k
# 1, if vehicle k drives directly from vertex i to vertex j 
x = m.addVars(cli,cli, veh, 
                name='x',
                vtype=GRB.BINARY) 
# print(x)

# variable si,k
# the time vehicle k starts to service customer i.
s = m.addVars(cli, veh, 
                name='s',
                vtype=GRB.CONTINUOUS)
# print(s)

# Constraints
m.addConstrs(
    x.sum(i,'*','*') == 1 for i in cli if i!=j
) 

m.addConstrs(
    quicksum(demand[i]*(quicksum(x[i,j,k]) for j in cli) for i in cli) <= cap
)


