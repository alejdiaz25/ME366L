import gurobipy as gp
from gurobipy import GRB

m = gp.Model("bus_drivers")

# data
d1, d2, d3, d4, d5, d6 = 11, 7, 18, 9, 16, 5
cP, cF, cS = 8, 12, 14
P, R, A = 8, 10, 20

# decision variables
# part-time (covers i)
p1 = m.addVar(lb=0, name="p1"); p2 = m.addVar(lb=0, name="p2"); p3 = m.addVar(lb=0, name="p3")
p4 = m.addVar(lb=0, name="p4"); p5 = m.addVar(lb=0, name="p5"); p6 = m.addVar(lb=0, name="p6")

# regular full-time (covers i, i+1)
f1 = m.addVar(lb=0, name="f1"); f2 = m.addVar(lb=0, name="f2"); f3 = m.addVar(lb=0, name="f3")
f4 = m.addVar(lb=0, name="f4"); f5 = m.addVar(lb=0, name="f5"); f6 = m.addVar(lb=0, name="f6")

# regular split-shift (covers i, i+2)
s1 = m.addVar(lb=0, name="s1"); s2 = m.addVar(lb=0, name="s2"); s3 = m.addVar(lb=0, name="s3")
s4 = m.addVar(lb=0, name="s4"); s5 = m.addVar(lb=0, name="s5"); s6 = m.addVar(lb=0, name="s6")

# premium full-time (covers i, i+1), costs 1.1*cF
g1 = m.addVar(lb=0, name="g1"); g2 = m.addVar(lb=0, name="g2"); g3 = m.addVar(lb=0, name="g3")
g4 = m.addVar(lb=0, name="g4"); g5 = m.addVar(lb=0, name="g5"); g6 = m.addVar(lb=0, name="g6")

# premium split-shift (covers i, i+2), costs 1.1*cS
h1 = m.addVar(lb=0, name="h1"); h2 = m.addVar(lb=0, name="h2"); h3 = m.addVar(lb=0, name="h3")
h4 = m.addVar(lb=0, name="h4"); h5 = m.addVar(lb=0, name="h5"); h6 = m.addVar(lb=0, name="h6")

# objective
m.setObjective(
    cP*(p1+p2+p3+p4+p5+p6)
    + cF*(f1+f2+f3+f4+f5+f6)
    + cS*(s1+s2+s3+s4+s5+s6)
    + 1.1*cF*(g1+g2+g3+g4+g5+g6)
    + 1.1*cS*(h1+h2+h3+h4+h5+h6),
    GRB.MINIMIZE)

# coverage constraints
m.addConstr(p1 + f1 + f6 + s1 + s5 + g1 + g6 + h1 + h5 >= d1, "period 1")
m.addConstr(p2 + f2 + f1 + s2 + s6 + g2 + g1 + h2 + h6 >= d2, "period 2")
m.addConstr(p3 + f3 + f2 + s3 + s1 + g3 + g2 + h3 + h1 >= d3, "period 3")
m.addConstr(p4 + f4 + f3 + s4 + s2 + g4 + g3 + h4 + h2 >= d4, "period 4")
m.addConstr(p5 + f5 + f4 + s5 + s3 + g5 + g4 + h5 + h3 >= d5, "period 5")
m.addConstr(p6 + f6 + f5 + s6 + s4 + g6 + g5 + h6 + h4 >= d6, "period 6")

# pool availability constraints
m.addConstr(p1+p2+p3+p4+p5+p6 <= P, "pool_parttime")
m.addConstr(f1+f2+f3+f4+f5+f6 + s1+s2+s3+s4+s5+s6 <= R, "pool_regular")
m.addConstr(g1+g2+g3+g4+g5+g6 + h1+h2+h3+h4+h5+h6 <= A, "pool_premium")

# solve
m.optimize()

print(f"\noptimal cost = {m.objVal}")
for v in m.getVars():
    print('Decision Variable %s = %g' % (v.varName, v.x))
print('Total Cost = %g' % (m.objVal))