import pandas as pd
import ast
import json
d = dict()
data = pd.read_csv('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_Traning Set (UQS Threshold = 50)_Transformer Format.csv')
for index, row in data.iterrows():
    labels = row['labels']
    labels = json.loads(labels)
    tokens = row['tokens']
    tokens = ast.literal_eval(tokens)
    target_group = row['Sentence Label + Target Group']
    target_group = target_group.split()
    target_group = target_group[2]
    tokens = [n.strip() for n in tokens]
    for l in range(len(labels)):
        if labels[l] == 1:
            word = tokens[l]
            beginning = l
            end = len(labels)
            r = end - beginning
            multi_flag = False
            for w in range(l + 1, r):
                if labels[w] == 2:
                    word = word + ' ' + tokens[w]
                    multi_flag = True
                else:
                    break

            if target_group not in d:
                d[target_group] = 1
            else:
                d[target_group] += 1
data = pd.read_csv('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_Test Set_Transformer Format.csv')
for index, row in data.iterrows():
    labels = row['labels']
    labels = json.loads(labels)
    tokens = row['tokens']
    tokens = ast.literal_eval(tokens)
    target_group = row['Sentence Label + Target Group']
    target_group = target_group.split()
    target_group = target_group[2]
    tokens = [n.strip() for n in tokens]
    for l in range(len(labels)):
        if labels[l] == 1:
            word = tokens[l]
            beginning = l
            end = len(labels)
            r = end - beginning
            multi_flag = False
            for w in range(l + 1, r):
                if labels[w] == 2:
                    word = word + ' ' + tokens[w]
                    multi_flag = True
                else:
                    break
            if target_group not in d:
                d[target_group] = 1
            else:
                d[target_group] += 1
dataframe = pd.DataFrame(d, index=[0])
dataframe.to_csv('Distribution of Target Spans per Target Group_HateXplain_Target Span Detection (Batches 1 - 120).csv')


