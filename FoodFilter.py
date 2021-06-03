import pandas as pd

# ===========================================================FOOD===========================================================

df = pd.read_csv('Datasets/Nutrition1.csv')
cols=df.columns
cols = cols.to_list()
rowCount = list(df.shape)[0]
cols.pop(0)
csv_Fooddata=[]
for data in range(rowCount):
    temp = []
    for column in cols:
        if pd.isna(df[column][data]):
            temp.append(0)
        elif '�' in str(df[column][data]):
            temp.append(float(str(df[column][data]).split('�')[0]))
        elif '<' in str(df[column][data]):
            temp.append(float(str(df[column][data]).split('<')[1]))
        else:
            temp.append(df[column][data])
    csv_Fooddata.append(tuple(temp))


# ===========================================================DISEASES===========================================================

df = pd.read_csv('Datasets/Medicines_output_herbal_medicines.csv')
diseases=dict()

for herbs,defect in zip(df['English common name of herbal substance'],df['Use']):
    if pd.isna(herbs):
        continue
    if ',' in defect:
        for dis in defect.split(','):
            dis = dis.strip(' ')
            try:
                diseases[dis].append(herbs)
            except KeyError:
                diseases[dis] = list([herbs])
    else:
        try:
            diseases[defect].append(herbs)
        except KeyError:
            diseases[defect] = list([herbs])


# ===========================================================DEFICIENCY===========================================================

df = pd.read_csv('Datasets/Deficiencies.csv')

deficit=[]


for disease,organ,deficiency in zip(df['Disease'],df['Organ affected'],df['Deficiency']):
    temp = []
    temp.append(disease)
    temp.append(organ)
    temp.append(deficiency)

    deficit.append(tuple(temp))
