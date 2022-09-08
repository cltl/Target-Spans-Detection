import random
import csv
import pandas as pd
df = pd.read_json ('HateXplain.json')
target_groups = pd.read_csv ('HateXplain target groups.csv', header=[0])
list_of_target_groups = target_groups['Target group'].tolist()
list_of_target_groups.remove('None')
import xlsxwriter

row = 1
column = 0
l = ['id', 'dataset', 'text', 'tokens', 'label']
workbook = xlsxwriter.Workbook('WholeDataSetHateXplainTargetingSortedTargets.xlsx', {'use_zip64': True})
worksheet = workbook.add_worksheet()

for i in range(len(l)):
    worksheet.write(0, i, l[i])
rationales = df.iloc[2]
post_ids = df.iloc[0]
annotators = df.iloc[1]
post_tokens = df.iloc[3]
count_row = 0
twitter_list_of_tuples = []
gab_list_of_tuples = []
from collections import Counter
all_targets = []
def find (counter):
    for key, value in counter.items():
        if value == 3:
            final = key
            return final
        else:
            if value == 2:
                final = key
                return final
            else:
                return "not found"
for target_group in list_of_target_groups:
    for i in range(len(post_tokens)):
        all_rationale = rationales[i]
        post_id = post_ids[i]
        sample = post_tokens[i]
        annotator = annotators[i]
        targets = []
        labels = []
        for ann in annotator:
            target = ann.get('target')
            target_string = ''
            for tt in target:
                target_string += tt
                target_string += ' '
            target_string.strip()
            label = ann.get('label')
            targets.append(target_string)
            labels.append(label)
        targets_counter = dict(Counter(targets))
        labels_counter = dict(Counter(labels))
        targets_counter = {k: v for k, v in sorted(targets_counter.items(), key=lambda item: item[1], reverse=True)}
        final_target = find(targets_counter)
        final_label= find(labels_counter)
        if final_target != 'not found' and final_label != 'not found' and final_label != 'normal':
            final_target = final_target.split()
            final_target = final_target[0]
            if final_target == target_group:
                sentence = ''
                tokens = ''
                sample_len = len(sample)
                if sample_len > 2 and sample_len < 61:
                    count_row += 1
                    count_len = 0
                    count_word = 0
                    for word in sample:
                        count_word += 1
                        count_len += 1
                        sentence += word
                        new_word = str(count_word) + "- " + word
                        tokens += new_word
                        if count_len != sample_len:
                            tokens += ', '
                            sentence += ' '
                    given_label = final_label + ' targeting ' + target_group
                    t = (post_id, 'HateXplain', sentence, tokens, given_label)
                    worksheet.write(count_row, 0, t[0])
                    worksheet.write(count_row, 1, t[1])
                    worksheet.write(count_row, 2, t[2])
                    worksheet.write(count_row, 3, t[3])
                    worksheet.write(count_row, 4, t[4])
workbook.close()
