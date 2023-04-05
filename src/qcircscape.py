from itertools import permutations
from qiskit import *
from qiskit.quantum_info import Statevector
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cmath import pi
import networkx as nx

# ****************************************************************************************************************************************

# Global settings

gateset_db = {0:['x','ccx'], 1:['h','s','cx'], 2:['h','t','cx'], 3:['p', 'rx', 'cx']}

system_size = 5             # Take as user input
min_length = 0              # Take as user input
max_length = 3              # Take as user input
gateset = gateset_db[3]     # Take as user input
qb_connectivity = 't'       # Take as user input

gateqbts = {'x':1, 'h':1, 't':1, 's':1, 'p':1, 'rx':1, 'cx':2, 'ccx':3}
gateargs = {}
gateperm = {}
opcodes = 0   
backend = Aer.get_backend('statevector_simulator')

# ****************************************************************************************************************************************

def qasm_id_to_prog(id0, cd):
    # id1 = Interpret id0 as a opcodes-digit number, of length max_length
    # id2 = Interpret id1 as composed of gateset on gateargs

    # print(id0,end=': ')
    id1 = []
    for _ in range(cd):
        dgt = id0%opcodes
        id0 = id0//opcodes
        id1.append(dgt)
    # print(id1)

    id2 = []
    for opid in id1:
        gid = 0
        pid = 0
        opid_tmp = opid
        while(opid_tmp > 0):
            if opid_tmp - gateperm[gateset[gid]] >= 0:
                opid_tmp -= gateperm[gateset[gid]]
                gid += 1                
            else:
                pid = opid_tmp
                break
        id2.append([gateset[gid],gateargs[gateset[gid]][pid]])
    # print(id2)
    return id2

def make_opcodes():

    global opcodes

    # Create connectivity graph
    if qb_connectivity == 't':
        edgelist = [(0,1), (1,2), (1,3), (3,4)]
    elif qb_connectivity == 'l':
        edgelist = [(0,1), (1,2), (2,3), (3,4)]
    elif qb_connectivity == 'c':                    # Complete graph
        edgelist = list(permutations(range(system_size),2))
    G = nx.from_edgelist(edgelist)

    for g in range(len(gateset)):
        if gateqbts[gateset[g]] == 1:
            perm = list(range(system_size)) # remains same
        else:
            perm_all = list(permutations(range(system_size),gateqbts[gateset[g]])) # for all n-qubit gates
            perm = []
            for mcg in perm_all:
                if nx.is_path(G, mcg):
                    perm.append(mcg)
        gateargs[gateset[g]] = perm
        gateperm[gateset[g]] = len(perm)
        opcodes += len(perm)

    # print("gateset:",gateset)
    # print("gateqbts:",gateqbts)
    # print("gateargs:",gateargs)
    # print("gateperm:",gateperm)

# ****************************************************************************************************************************************

def init_gen():
    possible_init = []
    for i in range(0,2**system_size):
        possible_init.append(format(i, f'0{system_size}b'))
    circ_init_list = []
    for pos in possible_init:
        oracle_circ = QuantumCircuit(system_size)
        for i in range(system_size):
            if(pos[-i-1]) == '1': # is this for qiskit convention?
                oracle_circ.x(i)
        circ_init_list.append(oracle_circ)
    return circ_init_list

# ****************************************************************************************************************************************

if __name__ == "__main__":

    opn_save = True
    opn_plot = True
    opn_plot_save = False
    show_progress = True

    if opn_plot:
        fig, axes = plt.subplots(2, max_length+1-min_length, figsize=(10, 10), sharey=True, sharex=True, subplot_kw=dict(aspect='equal'))

    print("\n****** Welcome to QCircScape! ******\n")

    # Prefix free code is not important, QASM should be unique, QASMs of same number of gates/runtime should be of same length
    # Assume no parallel scheduling, i.e. at every step, only 1 gate is performed (can be on any number of qubits)
    # Assume qubit ordering matters for all multi-qubit gates, i.e. cx[0,1], cx[1,0], cz[0,1], cz[1,0] are all unique

    init_circs = init_gen() 

    make_opcodes()
    
    for cd in range(min_length,max_length+1):
        qasm_id = opcodes**cd
        print("Total possible circuits of length",cd,":",qasm_id)
    
        pathsum = np.zeros((2**system_size, 2**system_size))
        for icno, ic in enumerate(init_circs):                  # Make into function
            if show_progress:
                print(cd,icno)
            for qid in range(qasm_id):
                if show_progress:
                    print(cd,icno,qid)
                qprog = qasm_id_to_prog(qid, cd)
                # print(qid,qprog)
                qcirc = QuantumCircuit(system_size)
                qcirc.barrier()
                # Add Init circuit here
                qcirc = qcirc.compose(ic)
                qcirc.barrier()
                for ins in qprog:
                    if ins[0] == 'x':
                        qcirc.x(ins[1])
                    elif ins[0] == 'h':
                        qcirc.h(ins[1])
                    elif ins[0] == 't':
                        qcirc.t(ins[1])
                    elif ins[0] == 's':
                        qcirc.t(ins[1])
                    elif ins[0] == 'p':         # Denotes p(pi/4)
                        qcirc.p(pi/4, ins[1])
                    elif ins[0] == 'rx':  # Denotes rx(pi/2)
                        qcirc.rx(pi, ins[1])
                    elif ins[0] == 'cx':
                        qcirc.cx(ins[1][0],ins[1][1])
                    elif ins[0] == 'ccx':
                        qcirc.ccx(ins[1][0],ins[1][1],ins[1][2])
                    qcirc.barrier()
                # print(qcirc.draw())
                job = execute(qcirc, backend, shots=1, memory=True)
                result = job.result()
                memory = Statevector(result.get_statevector(qcirc)).probabilities()
                # print(memory)
                # exit()
                for j in range(0,len(memory)):
                    pathsum[icno][j] += memory[j]
        
        gss = ''
        for g in gateset:
            gss += '-'+g
        gss = gss[1:]
            
        if opn_save:
            np.save(f'../data/info_Q-{system_size}_L-{cd}_GS-{gss}_CG-{qb_connectivity}', pathsum)
        
        if opn_plot:
            pathprob = np.divide(pathsum,sum(pathsum[0]))
            expressibility = 1*(pathsum != 0)
            # fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharey=True, sharex=True, subplot_kw=dict(aspect='equal'))
            sns.heatmap(expressibility, ax=axes[0][cd-min_length], cmap = 'YlOrBr', vmin=0.0, vmax=1.0, cbar = False, xticklabels = [], yticklabels = []) 
            sns.heatmap(pathprob, ax=axes[1][cd-min_length], cmap = 'YlOrBr', vmin=0.0, vmax=1.0, cbar = False, xticklabels = [], yticklabels = [])
            axes[0][cd-min_length].set_title(f'Depth: {cd}')
            # axes[1][cd].set_title(f'Reachability: Q-{system_size} Depth:{cd}')
    
    if opn_plot:
        fig.suptitle(f'Expressibility (top row) and Reachability (bottom row) of z-basis states on {system_size} qubits using gate set {gss}')        
        if opn_plot_save:
            plt.savefig(f'../data/plot_Q-{system_size}_L-{cd}_GS-{gss}.pdf')
        plt.show()

# ****************************************************************************************************************************************