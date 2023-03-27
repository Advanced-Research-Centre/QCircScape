from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

max_qubits = 40
max_depth = 40

gs_styles = [[1,3], [1,1,2]]
gs_names = ['{X, CCX}', '{H, S, CX} or {H, T, CX} or {U1(pi/4), RX(pi/2), CX}']

growth_db = np.zeros((len(gs_styles),max_qubits,max_depth))
for gstyl in range(len(gs_styles)):
    for q in range(max_qubits):
        for d in range(max_depth):
            opcodes = 0
            for g in gs_styles[gstyl]:
                if g == 1:
                    opcodes += q
                else:
                    opcodes += len(list(permutations(range(q),g))) 
            qasm_id = opcodes**d
            growth_db[gstyl][q][d] = qasm_id

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for gstyl in range(len(gs_styles)):
    for q in range(max_qubits):
        line = np.log(growth_db[gstyl][q])
        if gstyl == 0:
            gstyl0, = ax.plot(range(max_depth),q*np.ones(max_depth),line,':b',label = "gate tgts: [1,3]")
        else:
            gstyl1, = ax.plot(range(max_depth),q*np.ones(max_depth),line,':g',label = "gate tgts: [1,1,2]")
ax.set_xlabel('Circuit Depth')
ax.set_ylabel('Qubits')
ax.set_zlabel('Log # Programs')
ax.legend(handles=[gstyl0,gstyl1],loc='lower right')
plt.show()