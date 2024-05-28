#"from sets import Set"   Sets are built-in functions in Python3
import numpy as np
import Clusterpy
from pandas import *

# Total Municipios
colombia = Clusterpy.importArcData(
    "Oficial_Antioquia/Oficial_Antioquia") #"Oficial_Antioquia/Municipios_RIMISP"
data = len(colombia.Y.keys())
print('Total de municipios en el mapa: ', data)

# Leemos la matriz Dij
xls = ExcelFile('Oficial_Antioquia/diccionario_numeros.xls')
df = xls.parse(xls.sheet_names[0])
ind = df.set_index(['m']).to_dict()['i']

# csv.reader(open('Entradas/Oficial_Colombia/dij_def.csv'))
reader = read_csv('Oficial_Antioquia/dij_def_ant.csv')

Dij = dict()
for _, row in reader.iterrows():
    if len(row) >= 3:
        i, j, d1 = row[0], row[1], row[2]
        try:
            i_int = int(i)
            j_int = int(j)
        except ValueError:
            continue
        if i_int != 27086 and j_int != 27086 and i_int != 88001 and j_int != 88001 and i_int != 88564 and j_int != 88564:
            i = ind[i_int]
            j = ind[j_int]
            if i < j:
                Dij[i, j] = float(d1)
            elif i == j:
                Dij[i, j] = 0
    else:
        continue


reader = read_csv('Oficial_Antioquia/cij_def_ant.csv')

Cio = dict()
for _,row in reader.iterrows():
    if len(row) >= 3:
        i, j, d1 = row[0], row[1], row[2]
        try:
            i_int = int(i)
            j_int = int(j)
        except ValueError:
            continue
        
        if i_int != 27086 and j_int != 27086 and i_int != 88001 and j_int != 88001 and i_int != 88564 and j_int != 88564:
                i = ind[int(i)]
                j = ind[int(j)]
                if i != j:
                    Cio[i, j] = float(d1)
                elif i == j:
                    Cio[i, j] = 0
    else:
        pass

items = []
mpios = []
for item in Cio.keys():
    items.append(item[1])
    mpios.append(item[0])
items = set(items)
mpios = set(mpios)
# print('Municipios', len(mpios))
if data != len(mpios):
    print('La informacion de las distancias Cio no conicide con la informacion del mapa')

areas = []
print("Informacion de DIJ")
print(len(Dij))
print(data)
for area in Dij.keys():
    areas.append(area[1])
areas = set(areas)
print(len(areas))
if data != len(areas):
    print('La informacion de las distancias Dij no conicide con la informacion del mapa')

nd = np.zeros(len(areas)+1)
for potential in items:
    nd[potential] = 1

dn = {}
for _ in range(len(areas)):
    dn[_] = nd[_]
colombia.addVariable(['dn'], dn)

print("Ejecutando Modelos")
p = 2
colombia.cluster('pExhaustiveFunct  onalRegions', ['dn'], p, convTabu=int(len(
    areas)/p)*200, tabuLength=10, wType='rook', inits=10, dissolve=0, Dij=Dij, Cio=Cio)
colombia.exportArcData('Salidas/Colombia_int_'+str(p))
