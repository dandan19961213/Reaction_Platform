import os
from flask import Flask, render_template, send_from_directory, request, jsonify, Markup
import pandas as pd
import numpy as np
import json
from flask import request
# from dgl.data.utils import save_graphs
from flask_cors import CORS
from ase.visualize import view
from ase.db import connect
import pickle
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import random

app = Flask(__name__)
CORS(app, resources=r'/*')
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录
print(basedir)
ALLOWED_EXTENSIONS = set(['traj'])  # 允许上传的文件后缀

with open('C_H_all_reaction_without_H2O.txt', 'rb') as fp:
    r_ch = pickle.load(fp)
with open('CO_H2_products_all_reaction.txt', 'rb') as fp:
    p = pickle.load(fp)

db = connect("./qm9.db")
data = pd.read_csv("./QM9.csv")

rows = list(db.select(sort='id'))

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 主
# @app.route('/', methods=['GET', 'POST'])
# def upload_test():
#    # return render_template('user/homepage.html')
#    if request.method == 'GET':
#        return render_template('user/homepage.html', input_file='', res_text='')
#    else:
#        inputText = request.form.get("input_file")
#        resText = Markup(formatRes((inputText)))
#        return render_template('user/homepage.html', input_file=inputText, res_text=resText)

@app.route('/method1', methods=['POST'])
def return_table():
    item = json.loads(request.get_data(as_text=True))
    # print('item[text]111111111111', item)
    G = int(item['text1'][2:])
    g = item['text2']
    # print('GGGGGGGG', G)
    # print('ggggggggggg', g)
    res = []
    res1 = []
    res2 = []
    res3 = []
    res4 = []
    temp2 = {}
    temp4 = {}
    if g == str(('%.3f' % r_ch[G][4][6])):
        for i in range(2):
            temp1 = {}
            temp1['分子式'] = trans_symbols(r_ch[G][i])
            temp1['分子系数'] = r_ch[G][4][i * 2 + 1]
            temp1['Gibbs/eV'] = ('%.3f' % r_ch[G][4][i * 2])

            res1.append(temp1)
            # print(res1)
        temp2['分子式'] = trans_symbols(r_ch[G][2])
        temp2['分子系数'] = r_ch[G][4][5]
        temp2['Gibbs/eV'] = ('%.3f' % r_ch[G][4][4])

        res2.append(temp2)
        res.append(res1)
        res.append(res2)

        return {"tabledata": res}
    # print('1111', res)

    elif g == str(('%.3f' % p[G][4][6])):
        for i in range(2):
            temp3 = {}
            temp3['分子式'] = trans_symbols(p[G][i])
            temp3['分子系数'] = p[G][4][i * 2 + 1]
            temp3['Gibbs/eV'] = ('%.3f' % p[G][4][i * 2])

            res3.append(temp3)
            # print(res3)
        temp4['分子式'] = trans_symbols(p[G][2])
        temp4['分子系数'] = p[G][4][5]
        temp4['Gibbs/eV'] = ('%.3f' % p[G][4][4])
        res4.append(temp4)
        res.append(res3)
        res.append(res4)
        print('111111111111111111', res)

        return {"tabledata": res}


@app.route('/method2', methods=['POST'])
def return_qm9():
    item = json.loads(request.get_data(as_text=True))
    # print('item[text]2222222222', item['text'], item['text2'])
    # interval = item['text'].split('-')
    left = int(item['text']) - 1
    right = int(item['text2']) + int(item['text']) - 1

    res = []
    node = {}
    edge = {}
    link = []
    tableData = []
    edge_p = {}
    print('loop start')
    for i in range(left, right):
        node[str(r_ch[i][0])] = [trans_symbols(r_ch[i][0])]
        node[str(r_ch[i][1])] = [trans_symbols(r_ch[i][1])]
        node[str(r_ch[i][2])] = [trans_symbols(r_ch[i][2]), trans_xyz(r_ch[i][2])]

        element = []
        element.append(str(r_ch[i][4][1]) + trans_symbols(r_ch[i][0]))
        element.append(str(r_ch[i][4][3]) + trans_symbols(r_ch[i][1]))
        element.append(str(r_ch[i][2]))
        tableData.append(element)

        # print(tableData)

        edge[str(r_ch[i][0]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][0]))
        edge[str(r_ch[i][1]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][2]))
        edge[str(r_ch[i][2]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][4]))
        node['*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))] = str(('%.3f' % r_ch[i][4][6]))  # G：第几条反应

        link.append([str(r_ch[i][0]), edge[str(r_ch[i][0]) + '-' + str(i)], '*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))])
        link.append([str(r_ch[i][1]), edge[str(r_ch[i][1]) + '-' + str(i)], '*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))])
        link.append(['*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6])), edge[str(r_ch[i][2]) + '-' + str(i)], str(r_ch[i][2])])

        for j in range(len(p)):
            # print('pppppp', str(p[j][0]), str(p[j][1]))
            if str(r_ch[i][2]) == str(p[j][0]) or str(r_ch[i][2]) == str(p[j][1]):
                # print('yesyesyesyesyeysysysyyssysy')
                node[str(p[j][0])] = [trans_symbols(p[j][0]), trans_xyz(p[j][0])]
                node[str(p[j][1])] = [trans_symbols(p[j][1]), trans_xyz(p[j][1])]
                node[str(p[j][2])] = [trans_symbols(p[j][2]), trans_xyz(p[j][2])]

                edge_p[str(p[j][0]) + '-' + str(j)] = str(('%.3f' % p[j][4][0]))
                edge_p[str(p[j][1]) + '-' + str(j)] = str(('%.3f' % p[j][4][2]))
                edge_p[str(p[j][2]) + '-' + str(j)] = str(('%.3f' % p[j][4][4]))
                node['*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))] = str(('%.3f' % p[j][4][6]))

                link.append([str(p[j][0]), edge_p[str(p[j][0]) + '-' + str(j)], '*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))])
                link.append([str(p[j][1]), edge_p[str(p[j][1]) + '-' + str(j)], '*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))])
                link.append(['*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6])), edge_p[str(p[j][2]) + '-' + str(j)], str(p[j][2])])

    print('loop end')
    res.append([node])  # res[0] 物质的坐标模型
    res.append(link)   # res[0] 反应关系
    res.append(tableData)  # tableData 反应方程式
    # print('222222222222222',res)
    return {"tabledata": res}


@app.route('/method3', methods=['POST'])
def return_rand():
    print('co和h2的')
    item = json.loads(request.get_data(as_text=True))
    # print('item[text]333333', item)
    tmp = item['text']
    if int(tmp) == 0:
        randlist = random.sample(range(1, len(r_ch)), int(item['text2']))
    # print('randlist', randlist)

    res = []
    node = {}
    edge = {}
    link = []
    tableData = []
    edge_p = {}

    print('loop start')

    for i in randlist:
        node[str(r_ch[i][0])] = [trans_symbols(r_ch[i][0])]
        node[str(r_ch[i][1])] = [trans_symbols(r_ch[i][1])]
        node[str(r_ch[i][2])] = [trans_symbols(r_ch[i][2]), trans_xyz(r_ch[i][2])]
        # print(str(b[i][2]))

        element = []
        element.append(str(r_ch[i][4][1]) + trans_symbols(r_ch[i][0]))
        element.append(str(r_ch[i][4][3]) + trans_symbols(r_ch[i][1]))
        element.append(str(r_ch[i][2]))
        tableData.append(element)

        # print(tableData)

        edge[str(r_ch[i][0]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][0]))
        edge[str(r_ch[i][1]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][2]))
        edge[str(r_ch[i][2]) + '-' + str(i)] = str(('%.3f' % r_ch[i][4][4]))
        node['*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))] = str(('%.3f' % r_ch[i][4][6]))

        link.append([str(r_ch[i][0]), edge[str(r_ch[i][0]) + '-' + str(i)], '*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))])
        link.append([str(r_ch[i][1]), edge[str(r_ch[i][1]) + '-' + str(i)], '*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6]))])
        link.append(['*G' + str(i) + 'g' + str(('%.3f' % r_ch[i][4][6])), edge[str(r_ch[i][2]) + '-' + str(i)], str(r_ch[i][2])])

        for j in range(len(p)):
            # print('pppppp', str(p[j][0]), str(p[j][1]))
            if str(r_ch[i][2]) == str(p[j][0]) or str(r_ch[i][2]) == str(p[j][1]):
                # print('yesyesyesyesyeysysysyyssysy')
                node[str(p[j][0])] = [trans_symbols(p[j][0]), trans_xyz(p[j][0])]
                node[str(p[j][1])] = [trans_symbols(p[j][1]), trans_xyz(p[j][1])]
                node[str(p[j][2])] = [trans_symbols(p[j][2]), trans_xyz(p[j][2])]

                edge_p[str(p[j][0]) + '-' + str(j)] = str(('%.3f' % p[j][4][0]))
                edge_p[str(p[j][1]) + '-' + str(j)] = str(('%.3f' % p[j][4][2]))
                edge_p[str(p[j][2]) + '-' + str(j)] = str(('%.3f' % p[j][4][4]))
                node['*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))] = str(('%.3f' % p[j][4][6]))

                link.append([str(p[j][0]), edge_p[str(p[j][0]) + '-' + str(j)], '*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))])
                link.append([str(p[j][1]), edge_p[str(p[j][1]) + '-' + str(j)], '*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6]))])
                link.append(['*G' + str(j) + 'g' + str(('%.3f' % p[j][4][6])), edge_p[str(p[j][2]) + '-' + str(j)], str(p[j][2])])

    print('loop end')

    res.append([node])
    res.append(link)
    res.append(tableData)
    # print('3333333333333', res[0][0])
    return {"tabledata": res}

with open('Reactant_reactions_gibbs.txt','rb') as fp:
    b = pickle.load(fp)
with open('Reactant_reactions_hl.txt','rb') as fp:
    hl = pickle.load(fp)

@app.route('/method3_EG', methods=['POST'])
def return_rand_EG():
    item = json.loads(request.get_data(as_text=True))
    print('乙二醇的')
    # print(item['text'],item['text2'])
    tmp = item['text']
    if int(tmp) == 0:
        randlist = random.sample(range(1, len(b)), int(item['text2']))

    res = []
    node = {}
    edge = {}
    link = []
    print('loop start')
    for i in randlist:
        # str(b[i][0])物质的ID；trans_symbols(b[i][0])物质的化学式；trans_xyz(b[i][0])物质的坐标
        node[str(b[i][0])] = [trans_symbols(b[i][0]), trans_xyz(b[i][0])]
        node[str(b[i][1])] = [trans_symbols(b[i][1]), trans_xyz(b[i][1])]
        node[str(b[i][2])] = [trans_symbols(b[i][2]), trans_xyz(b[i][2])]

        # str(('%.3f' % b[i][4][0]))物质的吉布斯自由能
        edge[str(b[i][0]) + '-' + str(i)] = str(('%.3f' % b[i][4][0]))
        edge[str(b[i][1]) + '-' + str(i)] = str(('%.3f' % b[i][4][2]))
        edge[str(b[i][2]) + '-' + str(i)] = str(('%.3f' % b[i][4][4]))

        # '*G' + str(i)第几条反应；str(('%.3f' % b[i][4][6]))反应后的能量差
        node['*G' + str(i)] = str(('%.3f' % b[i][4][6]))

        # link(反应物id，反应物吉布斯自由能，第几条反应)
        link.append([str(b[i][0]), edge[str(b[i][0]) + '-' + str(i)], '*G' + str(i)])
        link.append([str(b[i][1]), edge[str(b[i][1]) + '-' + str(i)], '*G' + str(i)])
        # link(第几条反应，生成物布斯自由能，生成物ID）
        link.append(['*G' + str(i), edge[str(b[i][2]) + '-' + str(i)], str(b[i][2])])

    print('loop end')
    res.append([node])
    res.append(link)
    print(res)
    return {"tabledata": res}


def trans_symbols(atoms_id):
    if atoms_id == 140000:
        return 'CO'
    elif atoms_id == 140001:
        return 'H2'
    else:
        return str(rows[atoms_id - 1].toatoms().symbols)
    # for row in rows:
    #     atoms = row.toatoms()
    #     if row.id == id:
    #         return str(atoms.symbols)y


def trans_xyz(row_id):
    # print(data['SMILES1'])
    if row_id == 140001:
        pass
        # patt = Chem.MolFromSmiles('[H][H]')
    elif row_id == 140000:
        pass
        # patt = Chem.MolFromSmiles('C=O')
    else:
        smi = data['SMILES1'][row_id - 1]
        patt = Chem.MolFromSmiles(smi)
        m3 = Chem.AddHs(patt)
        AllChem.EmbedMolecule(m3, randomSeed=0xf00d)
        s = Chem.MolToXYZBlock(m3)
        s_list = s.split(" ")
        res = ""
        for i in s_list:
            res += str(i)
            res += ' '
        result = repr(res[:-2])
        return result

@app.route('/query_reaction', methods=['POST'])
def get_query_data():
    item = json.loads(request.get_data(as_text=True))
    print('查询获取的表单数据', item)
    print('species', item['species'])
    print('tem', item['temperature'])
    path = './video/'+item['temperature']+'.mp4'
    return{"path": path}

if __name__ == '__main__':
    # print(data)
    app.run(debug=True, host="0.0.0.0", port=8088)
