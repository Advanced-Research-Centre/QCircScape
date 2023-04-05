import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

system_size = 5
max_length = 3

gateset = ['p', 'rx', 'cx']

gss = ''
for g in gateset:
    gss += '-'+g
gss = gss[1:]

all_pathprob_L, all_pathprob_T = [], []

for plen in range(max_length+1):
    pathsum = np.load(f'../data/info_Q-{system_size}_L-{plen}_GS-{gss}_CG-l.npy')
    all_pathprob_L.append(np.divide(pathsum,sum(pathsum[0])))
    pathsum = np.load(f'../data/info_Q-{system_size}_L-{plen}_GS-{gss}_CG-t.npy')
    all_pathprob_T.append(np.divide(pathsum,sum(pathsum[0])))

M_L = np.zeros(np.shape(all_pathprob_L[0]))
M_T = np.zeros(np.shape(all_pathprob_T[0]))
for plen in range(1,max_length+1):
    M_L += ((2**-plen)*all_pathprob_L[plen-1])
    M_T += ((2**-plen)*all_pathprob_T[plen-1])

diff_M_L_T = np.subtract(M_L,M_T)   # Scale colours using this or 1.0

maxp_Mdiff = np.max(diff_M_L_T)
minp_Mdiff = np.min(diff_M_L_T)
scale_Mdiff = np.max(np.abs([maxp_Mdiff,minp_Mdiff]))

print(maxp_Mdiff,minp_Mdiff,scale_Mdiff)
maxp_M = np.max([np.max(M_L),np.max(M_T)])

fig, axes = plt.subplots(1, 3, figsize=(10, 10), sharey=True, sharex=True, subplot_kw=dict(aspect='equal'))
sns.heatmap(M_L, ax=axes[0], cmap = 'Blues', vmin=0.0, vmax=maxp_M, cbar = True, cbar_kws = dict(use_gridspec=False,location="bottom",pad=0.02), xticklabels = [], yticklabels = [])
axes[0].set_title(f'M_circ L')

s = sns.diverging_palette(120, 0, s=160, as_cmap=True)
sns.heatmap(diff_M_L_T, ax=axes[1], cmap = s, vmin=-scale_Mdiff, vmax=scale_Mdiff, cbar = True, cbar_kws = dict(use_gridspec=False,location="bottom",pad=0.02), xticklabels = [], yticklabels = [])
axes[1].set_title(f'M_circ diff')

sns.heatmap(M_T, ax=axes[2], cmap = 'Blues', vmin=0.0, vmax=maxp_M, cbar = True, cbar_kws = dict(use_gridspec=False,location="bottom",pad=0.02), xticklabels = [], yticklabels = [])
axes[2].set_title(f'M_circ T')

fig.suptitle(f'Difference of circuit probability on {system_size} qubits using gate set {gss} for depth {max_length} on IBM topology L and T')        
plt.show()