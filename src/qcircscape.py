from itertools import permutations
from qiskit import *
from qiskit.quantum_info import Statevector
import numpy as np

# ****************************************************************************************************************************************

# Global settings

system_size = 2
max_length = 2
gateset = ['h','t','cx']
gateqbts = {'h':1, 't':1, 'cx':2}
gateargs = {}
gateperm = {}
opcodes = 0   
backend = Aer.get_backend('statevector_simulator')

# ****************************************************************************************************************************************

def qasm_id_to_prog(id0):
    # id1 = Interpret id0 as a opcodes-digit number, of length max_length
    # id2 = Interpret id1 as composed of gateset on gateargs

    # print(id0,end=': ')
    id1 = []
    for _ in range(max_length):
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
    print("\n****** Welcome to QCircScape! ******\n")

    # Prefix free code is not important, QASM should be unique, QASMs of same number of gates/runtime should be of same length
    # Assume no parallel scheduling, i.e. at every step, only 1 gate is performed (can be on any number of qubits)
    # Assume qubit ordering matters for all multi-qubit gates, i.e. cx[0,1], cx[1,0], cz[0,1], cz[1,0] are all unique

    # List options at each time step
    for g in range(len(gateset)):
        if gateqbts[gateset[g]] == 1:
            perm = list(range(system_size))
        else:
            perm = list(permutations(range(system_size),gateqbts[gateset[g]])) 
        gateargs[gateset[g]] = perm
        gateperm[gateset[g]] = len(perm)
        opcodes += len(perm)
    # print("gateset:",gateset)
    # print("gateqbts:",gateqbts)
    print("gateargs:",gateargs)
    # print("gateperm:",gateperm)

    qasm_id = opcodes**max_length
    print("Total possible circuits of max length:",qasm_id)

    init_circs = init_gen()        
    AP = np.zeros((2**system_size, 2**system_size))

    for icno, ic in enumerate(init_circs):
        for qid in range(qasm_id):
            qprog = qasm_id_to_prog(qid)
            # print(qid,qprog)
            qcirc = QuantumCircuit(system_size)
            qcirc.barrier()
            # Add Init circuit here
            qcirc.compose(ic)
            qcirc.barrier()
            for ins in qprog:
                if ins[0] == 'h':
                    qcirc.h(ins[1])
                elif ins[0] == 't':
                    qcirc.t(ins[1])
                elif ins[0] == 'cx':
                    qcirc.cx(ins[1][0],ins[1][1])
                qcirc.barrier()
            # print(qcirc.draw())
            job = execute(qcirc, backend, shots=1, memory=True)
            result = job.result()
            memory = Statevector(result.get_statevector(qcirc)).probabilities()
            # print(memory)
            # exit()
            for j in range(0,len(memory)):
                AP[icno][j] += memory[j]
    
    print(AP)
        
# ****************************************************************************************************************************************