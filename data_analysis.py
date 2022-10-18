import copy
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as font_manager


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 12,
    'text.latex.preamble': r'\usepackage{amsfonts}'
})
# fig.suptitle('Matrices')

def aritra_matrix(op_step, qubit):
    M1 = np.load(f'data/info_qubit-{qubit}_prog_length-1.npy')
    M1 = np.divide(M1,sum(M1[0]))
    Mi = M1
    for _ in range(1,op_step):
        Mi = Mi@M1
    return Mi

def aritrar_boro_matrix(op_step, qubit):
    """
    Reachability 
    """
    M1 = np.load(f'data/info_qubit-{qubit}_prog_length-1.npy')
    M1 = np.divide(M1,sum(M1[0]))
    m = 0.5*M1
    Mi = M1
    for j in range(1,op_step):
        Mi = Mi@M1
        m += Mi*(2**(-(j+1)))
    return m

def expressibility_of_aritra(reachibility_matrix):
    """
    Expressibility
    """
    expressibility_matrix = copy.deepcopy(reachibility_matrix)
    for i in range(len(expressibility_matrix[0])):
        for j in range(len(expressibility_matrix[0])):
            if expressibility_matrix[i][j] == 0:
                expressibility_matrix[i][j] = 0
            else:
                expressibility_matrix[i][j] = 1
    return expressibility_matrix



if __name__ == "__main__":
    qubits = 3
    operations_length = 3

    if qubits < 4:
        xs, ys = 10, 10
    else:
        xs, ys = 3, 5

    fig, axes = plt.subplots(operations_length, 2, figsize=(xs, ys), sharey=True, sharex=True)

    for op_length in range(1, operations_length+1):
        reach_mat = aritrar_boro_matrix(op_length, qubits)
        exp_mat = expressibility_of_aritra(reach_mat)

        label = []

        if qubits < 4:
            for num in range(2**qubits):
                label.append(format(num, f'0{qubits}b'))
        
        sns.heatmap(exp_mat, ax=axes[op_length-1][0], xticklabels = label, yticklabels = label, cmap = 'Greens', vmin=0.0, vmax=1.0, cbar = False)
        sns.heatmap(reach_mat, ax=axes[op_length-1][1], xticklabels = label, yticklabels = label, cmap = 'Greens', vmin=0.0, vmax=1.0, cbar = False) 

    plt.tight_layout()
    if qubits < 4:
        axes[0][0].set_title('Expressibility')
        axes[0][1].set_title('Reachability')
    plt.savefig(f'plot/quantum_reach_and_expressibility_qubit_{qubits}.pdf')
    plt.savefig(f'plot/quantum_reach_and_expressibility_qubit_{qubits}.png')

    plt.show()