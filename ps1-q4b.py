import gurobipy as gp
from gurobipy import GRB

m = gp.Model("panel_cut")

x1 = m.addVar(vtype='C', lb=0, name="x1")
x2 = m.addVar(vtype='C', lb=0, name="x2")
x3 = m.addVar(vtype='C', lb=0, name="x3")
x4 = m.addVar(vtype='C', lb=0, name="x4")
x5 = m.addVar(vtype='C', lb=0, name="x5")
x6 = m.addVar(vtype='C', lb=0, name="x6")

m.setObjective(x1 + x2 + x3 + x4 + x5 + x6, GRB.MINIMIZE)

m.addConstr(2*x1 + x2 + x3 == 30, "panel A")
m.addConstr(2*x1 + 3*x2 + x3 + 4*x4 + 2*x5 == 50, "panel B")
m.addConstr(x3 + x5 + 2*x6 == 20, "panel C")

m.optimize()

for v in m.getVars():
    print('Decision Variable %s = %g' % (v.varName, v.x))
print('sheets = %g' % (m.objVal))