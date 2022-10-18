import copy
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
fig.suptitle('Matrices')

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

    reach_mat = aritrar_boro_matrix(operations_length, qubits)
    exp_mat = expressibility_of_aritra(reach_mat)

    label = []
    for num in range(2**qubits):
        label.append(format(num, f'0{qubits}b'))
        # label.append("{0:b}".format(num))

    sns.heatmap(exp_mat, ax=axes[0], xticklabels = label, yticklabels = label, cmap = 'Greens', vmin=0.0, vmax=1.0)
    axes[1].set_title('Expressibility')

    sns.heatmap(reach_mat, ax=axes[1], xticklabels = label, yticklabels = label, cmap = 'Greens', vmin=0.0, vmax=1.0) 
    axes[0].set_title('Reachability')

# sns.heatmap(reach_mat, cmap = 'Greens', vmin=0.0, vmax=1.0)
# plt.savefig( 'plot/reachability_matrix.pdf')
# plt.savefig( 'plot/reachability_matrix.png')

# sns.heatmap(exp_mat, cmap = 'Greens', vmin=0.0, vmax=1.0)
# plt.savefig( 'plot/expressibility_matrix.pdf')
# plt.savefig( 'plot/expressibility_matrix.png')

        # xticklabels=qc1.columns,
        # yticklabels=qc1.columns)
plt.show()

# l = []
# for i in range(2**qubit):
#     for j in range(2**3):
#         if (qc1@qc1)[i][j] == qc2[i][j]:
#             l.append(0)
#         else:
#             l.append(1)
# if sum(l) == 0:
#     print(' (prog_length-1 X prog_length-1) = prog_length-2')
# else:
#     print('no correlation')