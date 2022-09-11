import pandas as pd
ids = []
words = []
labels = []
s_ts = []
df = pd.read_excel ('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_Test Set.xlsx', header=[0])
new_df = pd.DataFrame()
import ast
columns = ['id', 'tokens', 'labels', 'Sentence Label + Target Group']
for index, row in df.iterrows():
    id = row['ID']
    id = id.split('_')
    id = id[1] + '_' + id[2]
    if id not in ids:
        if len(ids) != 0:
            previous_id = ids[-1]
            s_t = row['Sentence Label + Target Group']
            s_ts.append(s_t)
            data = [[previous_id, words, labels, s_t]]
            data2 = pd.DataFrame(data, columns=columns)
            new_df = new_df.append(data2)
            words = []
            labels = []
            ids.append(id)
            word = row['Token'].split('- ')
            word = word[1]
            words.append(word)
            label = row['IOB Label']
            labels.append(label)
        else:
            word = row['Token'].split('- ')
            word = word[1]
            words.append(word)
            label = row['IOB Label']
            labels.append(label)
            ids.append(id)
    else:
        word = row['Token'].split('- ')
        word = word[1]
        words.append(word)
        label = row['IOB Label']
        labels.append(label)
print('qeafdsesd')
data = [[ids[-1], words, labels, s_ts[-1]]]

data2 = pd.DataFrame(data, columns=columns)
print(data2)
new_df = new_df.append(data2)
print(new_df)
new_df.to_csv('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_Test Set_Transformer Format.csv')



