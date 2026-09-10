import gurobipy as gp
from gurobipy import GRB

m = gp.Model("giapetto")

x1 = m.addVar(vtype='C', lb=0, name="soldiers")   # soldiers/week
x2 = m.addVar(vtype='C', lb=0, name="trains")     # trains/week

m.setObjective(3*x1 + 2*x2, GRB.MAXIMIZE)

m.addConstr(2*x1 + x2 <= 100, "finishing")
m.addConstr(x1 + x2 <= 80,    "carpentry")
m.addConstr(x1 <= 40,         "demand")

m.optimize()

for v in m.getVars():
    print('Decision Variable %s = %g' % (v.varName, v.x))
print('profit/week = %g' % (m.objVal))