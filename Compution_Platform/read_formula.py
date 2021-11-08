import pickle
import rdkit
import csv
from rdkit import Chem
from rdkit.Chem import Draw

import pandas as pd
data = pd.read_csv("QM9.csv")

# print(data['SMILES1'][0])
check = []
with open('C_H_all_reaction_without_H2O.txt', 'rb') as fp:
#with open('Reactant_reactions_all.txt', 'rb') as fp:
    b = pickle.load(fp)
# print(b[0])
for i in range(len(b)):
        if b[i][2] not in check:
            smi = data['SMILES1'][b[i][2]-1]
            m = Chem.MolFromSmiles(smi)
            f = '/root/lidan/Ethylene_glycol_reaction/Aliyun/EGRComputingPlatform/picture' + str(b[i][2]) + '.png'
            #f = '/data/tp/picture01/' + str(b[i][2]) + '.png'
            #f = str(b[i][j]) + '.png'
            Draw.MolToFile(m, f, size=(150, 100))
            check.append(b[i][2])
print(len(check))
