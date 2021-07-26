import pandas as pd

Node = []
R_Cord = []
T_Cord = []
T_180 = []
Z_Cord = []
VM_0 = []
VM_180 = []
Sa = []
Sm = []
Sa0 = []

with open('Hub Stresses REV1.csv', 'r') as in_file:
    for i,line in enumerate(in_file):
        if i == 0:
            pass
        elif line[0] == ',':
            pass
        else:
            line = line.split(",")
            Node.append(line[0])
            R_Cord.append(float(line[1]))
            T_Cord.append(float(line[2]))
            Z_Cord.append(float(line[5]))
            VM_0.append(float(line[7]))


T_180 = [x + 180 if x < 0 else x - 180 for x in T_Cord]
VM_180 = [None]*len(VM_0)
Sa = [None]*len(VM_0)
Sm = [None]*len(VM_0)
Sa0 = [None]*len(VM_0)

def match(target,target2):
    zcords = []
    i_zcords = []
    tcords = []
    i_tcords = []
    for i,z in enumerate(Z_Cord):
        if target-0.2 <= z <= target + 0.2: #use approx 0.2 for fine mesh. trial and error to find lowest numbers that find matches. 0.9 for coarse
            zcords.append(z)
            i_zcords.append(i)
    for i,T in enumerate(T_Cord):
        if target2-0.50 <= T <= target2 + 0.50: #use approx 0.5 is appropriate for fine mesh. good idea to measure angle between adjacent nodes. 4.5 for coarse
            tcords.append(T)
            i_tcords.append(i)
    return list(set(i_zcords) & set(i_tcords))[0]

for i in range(0,len(VM_0)):
    VM_180[i] = VM_0[match(Z_Cord[i],T_180[i])]

#VM_180[0] = VM_0[match(-104,0)]

dict = {'Node': Node, 'R Coord': R_Cord, 'T Coord': T_Cord, 'T 180 Coord':T_180,
        'Z Coord':Z_Cord,'VM 0':VM_0,'VM 180':VM_180,'Sa':Sa,'Sm':Sm,'Sa0':Sa0}     

df = pd.DataFrame(dict)

df["Sa"] = (df["VM 0"] - df["VM 180"]) / 2
df["Sm"] = (df["VM 0"] + df["VM 180"]) / 2

Ftu = 1100 # MPa

df["Sa0"] = df["Sa"]/(1-(df["Sm"]/Ftu))

df.to_excel("Hub_Stresses_Python.xlsx")
