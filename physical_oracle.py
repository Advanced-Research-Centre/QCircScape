from cmath import pi
from qiskit import *
import itertools
import numpy as np
from qiskit.quantum_info import Statevector

# gate set:

# gate_list = [U(lamda), RX(pi/2), CNOT]


"""
We have to construct oracle using these three gates as per hardware.
Dui line code (two line code): [U, CX], [U, RX], [RX, CX]
Increase line of code:
"""

def toStr(n,base):
    '''
    Convert a decimal number to base-n
    '''
    convertString = "0123456789ABCDEF"
    if n < base:
        return convertString[n]
    else:
        return toStr(n//base,base) + convertString[n%base]


def aritra_dar_initialization(possible_init, size_of_aritra):
    """
    possible_init = all possible initializations e.g. 4 qubit ['0000', '0001', ....]
    size_of_aritra = this is the size of the system.
    """
    circ_init_list = []
    for pos in possible_init:
        oracle_circ = QuantumCircuit(size_of_aritra)
        for i in range(size_of_aritra):
            if(pos[-i-1]) == '1': # is this for qiskit convention?
                oracle_circ.x(i)
        circ_init_list.append(oracle_circ)
    return circ_init_list

def one_qubit_choice(aritra_da_bhibhajito, gs_opcode):
    ''' 
    aritra_da_bhibhajito = len(system dimension) e.g.[0,1,2,3]
    gs_opcode = choice of operation
    '''
    c = list(itertools.combinations(aritra_da_bhibhajito, 1))
    print(c)
    allc = []
    for i in c:
        allc.append(gs_opcode+str(i[0]))
    return allc

def two_qubit_choice(aritra_da_bhibhajito, gs_opcode):
    ''' 
    aritra_da_bhibhajito = len(system dimension) e.g.[0,1,2,3]
    gs_opcode = choice of operation
    '''
    c = list(itertools.combinations(aritra_da_bhibhajito, 2))
    allc = []
    for i in c:
        allc.append(gs_opcode+str(i[0])+str(i[1]))
        allc.append(gs_opcode+str(i[1])+str(i[0]))
    return allc

def program_generator(gc, setU1, setRX, setCX):
    ''' 
    gc = length of program = number of operations

    '''
    p = []
    if gc == 0:
        return p
    for i in range(0,len(gs)**gc):
        gseq = toStr(i,len(gs)).zfill(gc)
        cg = ['']          
        for j in range(0, len(gseq)):
            if gseq[j] == '0':
                g = list(itertools.product(cg, setU1))
            elif gseq[j] == '1':
                g = list(itertools.product(cg, setRX))
            elif gseq[j] == '2':
                g = list(itertools.product(cg, setCX))
            cg = []
            for k in g:
                cg.append(''.join(map(str, k)))
        for j in cg:
            p.append(j)
    return p


def runQprog(size_of_aritra, prog_desc, list_init_circ):
    AP = np.zeros((2**size_of_aritra, 2**size_of_aritra))
    for desc in prog_desc:
        for init_no, init in enumerate(list_init_circ):
            qcirc = QuantumCircuit(size_of_aritra)
            # print(init)
            qcirc = qcirc.compose(init)
            qcirc.barrier()
            i = 0
            while (i < len(desc)):
                if desc[i]=='0':
                    qcirc.u1(pi/4, int(desc[i+1]))
                    i+= 2
                elif desc[i]=='1':
                    qcirc.rx(pi, int(desc[i+1]))
                    i+= 2
                elif desc[i]=='2':
                    qcirc.cx(int(desc[i+1]),int(desc[i+2]))
                    i+= 3
            qcirc.barrier()
            job = execute(qcirc, backend, shots=1, memory=True)
            result = job.result()
            memory = Statevector(result.get_statevector(qcirc)).probabilities()
            for j in range(0,len(memory)):
                if memory[j] > 0:
                    AP[init_no][j] += memory[j]
            # print(qcirc)
    return AP


if __name__ == "__main__":
    backend = Aer.get_backend('statevector_simulator')
    size_of_aritra = 3
    aritra_da_bhibhajito = list(range(0,size_of_aritra))
    gs = ['u1(pi/4)', 'rx(pi/4)', 'cx']
    gs_opcode = ['0', '1', '2']
    gc = 3
    
    setU1 = one_qubit_choice(aritra_da_bhibhajito, gs_opcode[0])
    setRX = one_qubit_choice(aritra_da_bhibhajito, gs_opcode[1])
    setCX = two_qubit_choice(aritra_da_bhibhajito, gs_opcode[2])

    program_description = program_generator(gc, setU1, setRX, setCX)

    possible_states = []
    for i in range(0,2**size_of_aritra):
        possible_states.append(format(i, f'0{size_of_aritra}b'))
    circ = QuantumCircuit(4)
    list_init_circ = aritra_dar_initialization(possible_states, size_of_aritra)
    final_mat = runQprog(size_of_aritra, program_description, list_init_circ)
    np.save(f'data/info_qubit-{size_of_aritra}_prog_length-{gc}', final_mat)


"""
gc = 1
[[18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]
 [18.   0.5  0.5  0.   0.5  0.   0.   0.   0.5  0.   0.   0.   0.   0.
   0.   0. ]]


gc = 2
[[323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]
 [323.   17.   17.    1.5  17.    1.5   1.5   0.   17.    1.5   1.5   0.
    1.5   0.    0.    0. ]]
"""