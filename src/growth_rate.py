print("\n****** Welcome to Growth Rate Investigation! ******\n")

# ****************************************************************************************************************************************

import itertools
import pickle


def growth_rate( gatecode, qubit ):
    system_size = qubit
    gateargs = {}
    gateperm = {}
    opcodes = 0


    if gatecode == [1,3]:
        gateset = ['x', 'ccx']
        gateqbts = {'x':1, 'ccx':3}
    elif gatecode == [1,1,2]:
        gateset = ['h', 't', 'cx']
        gateqbts = {'h':1, 't':1, 'cx':2}

    for g in range(len(gateset)):
        if gateqbts[gateset[g]] == 1:
            perm = list(range(system_size))
        else:
            perm = list(itertools.permutations(range(system_size),gateqbts[gateset[g]])) 
        gateargs[gateset[g]] = perm
        gateperm[gateset[g]] = len(perm)
        opcodes += len(perm)
    return opcodes


if __name__ == "__main__":
    
    total_qubits = 100
    gate_code_list = [ [1,3], [1,1,2]  ]
    prog_num_dict = {f'{gate_code_list[0]}': [], f'{gate_code_list[1]}': []}
    for gateset in gate_code_list:
        for qubit in range(3, total_qubits+1):
            prog_numb = growth_rate( gateset, qubit )
            prog_num_dict[f'{gateset}'].append(prog_numb)
            print(gateset, qubit, 'DONE!')
    with open(f'../data/INFO_prog_numb.p', 'wb') as fp:
        pickle.dump(prog_num_dict, fp)