import ase
from ase.db import connect
import numpy as np
import itertools
import multiprocessing
from base64 import b64encode, b64decode
import schnetpack as spk
from schnetpack.datasets import QM9

G = "free_energy"
multi_thd = False
qm9data = QM9('./qm9.db', download=False, load_only=[QM9.G], remove_uncharacterized=True)
atomrefs = qm9data.get_atomref(QM9.G)

G_H = '{:.10f}'.format(atomrefs[QM9.G][1][0])
G_C = '{:.10f}'.format(atomrefs[QM9.G][6][0])
G_O = '{:.10f}'.format(atomrefs[QM9.G][8][0])

db = connect('./qm9.db')
# rows = list(db.select(sort='id'))
rows = list(db.select('id<50'))

atom_names = ['H', 'C', 'O', 'F', 'N']
atom_dict = {'H': 0, 'C':1, 'O':2, 'F':3, 'N':4}
atom_cnt_lst = []
atom_cnt_dict = {}
label = []

def hash_1d_array(arr):
    ret = 0
    arr = list(arr)
    for i in range(len(arr)):
        ret += (arr[i] * pow(50, (len(arr) - i)))
    return ret

def multi_thd_reac(reac_lst_orig, xishu):
    ret = reac_lst_orig
    # print('reac_lst_orig', reac_lst_orig)
    # print(reac_lst_orig[2])
    k = xishu[0]
    p = xishu[1]
    q = xishu[2]
    g1 = -1.4265472
    g2 = 0
    at, props = qm9data.get_properties(idx = reac_lst_orig[2] -1)
    # print('at', at)
    # print('props', props)

    at_num = at.numbers
    H_num = 0
    C_num = 0
    O_num = 0
    for i in range(len(at_num)):
        if at_num[i] == 1:
            H_num += 1
        elif at_num[i] == 6:
            C_num += 1
        else:
            O_num += 1
    g3 = props[QM9.G].cpu().numpy()[0] - float(G_H) * H_num - float(G_C) * C_num - float(G_O) * O_num

    if (g1 * k + g2 * p - g3 * q > 0):  # A + B => C
        ret.append(1)
    else:
        ret.append(-1)  # C => A + B
    # ret.append(g3)
    ret.append([g1, k, g2, p, g3 , q, g3 * q - g1 * k - g2 * p])

    return ret

if __name__ == '__main__':
    co_id = 140000
    atom_cnt_co = [0, 1, 1, 0, 0]
    atom_cnt_lst.append(np.array(atom_cnt_co))
    k_co = hash_1d_array(np.array(atom_cnt_co))
    atom_cnt_dict[k_co] = [co_id]

    h2_id = 140001
    atom_cnt_h2 = [2, 0, 0, 0, 0]
    atom_cnt_lst.append(np.array(atom_cnt_h2))
    k_h2 = hash_1d_array(np.array(atom_cnt_h2))
    atom_cnt_dict[k_h2] = [h2_id]

    for row in rows:
        at = row.toatoms()
        atom_cnt = [0] * len(atom_names)
        for a in at:
            atom_cnt[atom_dict[a.symbol]] += 1
        atom_cnt_lst.append(np.array(atom_cnt))
        k = hash_1d_array(np.array(atom_cnt))
        if (atom_cnt_dict.__contains__(k)):
            atom_cnt_dict[k].append(row.id)
        else:
            atom_cnt_dict[k] = [row.id]
    # print('atom_cnt_lst', atom_cnt_lst)
    # print('atom_cnt_dict', atom_cnt_dict)

    dk = list(atom_cnt_dict.keys())
    reac_cnt = 0
    reac_lst = []
    symbol = 0

    for i in range(len(dk)):
        for k in range(1, 100):
            for p in range(1, 100):
                for q in range(1, 100):
                    if (atom_cnt_dict.__contains__(k_co * k + k_h2 * p)):
                        if  k_co * k + k_h2 * p == dk[i] * q:

                            reac_cnt += (len(atom_cnt_dict[k_co]) * len(atom_cnt_dict[k_h2]) * len(atom_cnt_dict[dk[i]]))

                            s = [atom_cnt_dict[k_co], atom_cnt_dict[k_h2], atom_cnt_dict[dk[i]]]
                            xishu = [k, p, q]

                            reac_lst_idx = []
                            reac_lst_idx += list(itertools.product(*s))

                            reac_lst_res = []
                            reac_lst_res.extend((reac_lst_idx, xishu))
                            reac_lst.append(reac_lst_res)
                            symbol = 1
            if symbol == 1:
                symbol = 0
                break
    # print('reac_lst', reac_lst)

    for i in range(len(reac_lst)):
        for j in range(len(reac_lst[i])-1):
            for k in range(len(reac_lst[i][j])):
                reac_lst[i][j][k] = list(reac_lst[i][j][k])
    # print('reac_lst', reac_lst)

    reac_lst_1 = []
    temp = []

    for m in range(len(reac_lst)):
        if(multi_thd):
            pool = multiprocessing.Pool(2)
            reac_lst_1 = pool.map(multi_thd_reac, reac_lst[m][0],reac_lst[m][1])
            temp = reac_lst_1
        else:
            for z in reac_lst[m][0]:
                reac_lst_1.append(multi_thd_reac(z,reac_lst[m][1]))
            temp = reac_lst_1
    print('temp', temp, len(temp))

    import pickle
    with open('C_H_all_reaction_without_H2O.txt', 'wb') as fp:
        pickle.dump(temp, fp)
