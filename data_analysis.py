import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def aritra_matrix(op_step, qubit):
    M1 = np.load(f'data/info_qubit-{qubit}_prog_length-1.npy')
    M1 = np.divide(M1,sum(M1[0]))
    Mi = M1
    for _ in range(1,op_step):
        Mi = Mi@M1
    return Mi

def aritrar_boro_matrix(op_step, qubit):
    M1 = np.load(f'data/info_qubit-{qubit}_prog_length-1.npy')
    M1 = np.divide(M1,sum(M1[0]))
    m = 0.5*M1
    Mi = M1
    for j in range(1,op_step):
        Mi = Mi@M1
        m += Mi*(2**(-(j+1)))
    return m



sns.heatmap(aritrar_boro_matrix(3,3), cmap = 'Greens', vmin=0.0, vmax=1.0)
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