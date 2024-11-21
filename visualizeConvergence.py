import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def count_num_clause_in_one_epoch(clauses_in_one_epoch, states):
    number_of_clause = int((len(clauses_in_one_epoch)-1) / 4)
    sub_pattern = np.zeros(4)
    for i in range(number_of_clause):
        if clauses_in_one_epoch[i*4] >= states:
            if clauses_in_one_epoch[i*4+2] >= states:
                if clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+3] < states:
                    sub_pattern[3] += 1
            if clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+2] < states and clauses_in_one_epoch[i*4+3] < states:
                sub_pattern[3] += 1
        if clauses_in_one_epoch[i*4+2] >= states:
            if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+3] < states:
                sub_pattern[3] += 1

        if clauses_in_one_epoch[i*4+1] >= states:
            if clauses_in_one_epoch[i*4+3] >= states:
                if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+2] < states:
                    sub_pattern[0] += 1
            if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+2] < states and clauses_in_one_epoch[i*4+3] < states:
                sub_pattern[0] += 1
        if clauses_in_one_epoch[i*4+3] >= states:
            if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+2] < states:
                sub_pattern[0] += 1

        if clauses_in_one_epoch[i*4+1] >= states:
            if clauses_in_one_epoch[i*4+2] >= states:
                if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+3] < states:
                    sub_pattern[1] += 1
            if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+2] < states and clauses_in_one_epoch[i*4+3] < states:
                sub_pattern[1] += 1
        if clauses_in_one_epoch[i * 4 + 2] >= states:
                if clauses_in_one_epoch[i * 4] < states and clauses_in_one_epoch[i * 4 + 1] < states and clauses_in_one_epoch[i * 4 + 3] < states:
                    sub_pattern[1] += 1

        if clauses_in_one_epoch[i*4] >= states:
            if clauses_in_one_epoch[i*4+3] >= states:
                if clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+2] < states:
                    sub_pattern[2] += 1
            if clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+2] < states and clauses_in_one_epoch[i*4+3] < states:
                sub_pattern[2] += 1
        if clauses_in_one_epoch[i*4+3] >= states:
                if clauses_in_one_epoch[i*4] < states and clauses_in_one_epoch[i*4+1] < states and clauses_in_one_epoch[i*4+2] < states:
                    sub_pattern[2] += 1
    return sub_pattern



# df = pd.read_excel('../01AND E400Smp100T8S4C7.xlsx', header=None)
#df = pd.read_excel('Case OR Clause out per epoch T=2.xlsx', header=None)
df = pd.read_excel('AND irrelevant C5_T2_S3_th_2 Epoch20 sample 20.xlsx', header=None)
print(df.head())

data = df.values
# print(data.shape, data.dtype)
num_clause = np.zeros((data.shape[0], 4))
for i in range(data.shape[0]):
    num_clause[i, :] = count_num_clause_in_one_epoch(clauses_in_one_epoch=data[i, :data.shape[1]], states=101)

# print(num_clause)

# fig, ax = plt.subplots(5, 1, figsize=(15, 12))
# for i in range(4):
#     ax[i].plot(num_clause[:200, i])
# ax[4].plot(data[:, -1])
# ax[0].set_title('[$x_1$, $x_2$] = [0, 0]')
# # ax[0].gca().yaxis.set_major_locator(MaxNLocator(integer=True))
# ax[1].set_title('[$x_1$, $x_2$] = [0, 1]')
# ax[2].set_title('[$x_1$, $x_2$] = [1, 0]')
# ax[3].set_title('[$x_1$, $x_2$] = [1, 1]')
# ax[4].set_title('number of updates')

line_type = ['*', '.', '+', 'x']
label = ['[$x_1$, $x_2$] = [0, 0]', '[$x_1$, $x_2$] = [0, 1]', '[$x_1$, $x_2$] = [1, 0]', '[$x_1$, $x_2$] = [1, 1]']
fig1, ax1 = plt.subplots(2, 1, figsize=(9,6))
for i in range(4):
    ax1[0].plot(num_clause[:, i], line_type[i], label = label[i])
ax1[0].legend(fontsize='x-large', loc='upper right')
ax1[0].set_ylabel('The number of clauses', fontsize='x-large')
# ax1[0].set_ylim((-0.2, 6.2))
ax1[1].plot(data[:, -1])
# ax1[1].legend()
ax1[1].set_ylabel('The number of updates', fontsize='x-large')
plt.xlabel('Epochs', fontsize='x-large')
# plt.savefig('../TM_AND_OR/01AND E400Smp100T8S4C7.eps')
# plt.savefig('../TM_AND_OR/01AND E400Smp100T8S4C7.pdf')
plt.show()

print('end')