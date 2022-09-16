import pandas as pd
from pathlib import Path
data = pd.read_csv("/annotation results/batch 23/results including gold data (removed duplicates).csv", header = [0])
#data = pd.read_csv("/annotation results/batch 2/results including gold data.csv", header = [0])
row = 1
column = 0
import xlsxwriter
l = ['token', 'UQS', 'final label']
workbook = xlsxwriter.Workbook('/annotation results/batch 23/final labels (gold data).xlsx')
#workbook = xlsxwriter.Workbook('/annotation results/batch 2/final labels (gold data).xlsx')
worksheet = workbook.add_worksheet()
for i in range(len(l)):
    worksheet.write(0, i, l[i])
data_top = list(data.head())
data_top.remove('listnumber')
data_top.remove('assignmentid')
data_top.remove('hitid')
data_top.remove('origin')
data_top.remove('partid')
data_top.remove('id')
data_top.remove('questionid')
data_top[2] = "_started_at"
data_top[3] = "selected_answer"
data_top[8] = '_id'
data_top[6] = '_unit_id'
data_top[1] = '_worker_id'
data_top[4] = 'dataset'
data_top.append('_created_at')
list_of_months = {'Jan':'01',
'Feb':'02',
'Mar':'03',
'Apr':'04',
'May':'05',
'Jun':'06',
'Jul':'07',
'Aug':'08',
'Sep':'09',
'Oct':'10',
'Nov':'11',
'Dec':'12'}
list_of_texts = data['text'].to_list()
texts = sorted(list(set(list_of_texts)))
list_of_anotators_and_submissiontime = []
approved_workerids = ['Piek', 'BaranBarbarestani', 'Isa']
counter_approved_id = 0
found = False
for approved_workerid in approved_workerids:
    found = False
    for index, row in data.iterrows():
        if approved_workerid == row['workerid']:
            id = approved_workerid
            time_and_date = row['timestamp']
            time_and_date = time_and_date.split()
            date = time_and_date[0]
            date = date.split('-')
            day = date[0]
            month = date[1]
            month = list_of_months[month]
            year = date[2]
            new_date = year + '-' + month + '-' + day
            submission_time = time_and_date[1]
            submission_time = submission_time.split(':')
            hour = submission_time[0]
            submission_hour = str(int(hour) + 1)
            minute = '00'
            second = '00'
            submission_time = submission_hour + ':' + minute + ':' + second
            started_hour = str(int(hour) - 1)
            started_time = started_hour + ':' + minute + ':' + second
            annotator_time = (id, started_time, submission_time, new_date)
            list_of_anotators_and_submissiontime.append(annotator_time)
            break
    if found == True:
        break
list_of_dataframes = []
count = 0
def tokenization (text):
    for index, row in data.iterrows():
        if row['text'] == text:
            tokens = row['answer']
            new_answer = tokens.split(',\\"')
            new_answer2 = []
            for j in new_answer:
                newj = j.replace('\\"', '')
                newj = newj.replace('"{', '')
                newj = newj.replace('}"', '')
                new_answer2.append(newj.strip())
            new_tokens = []
            for k in new_answer2:
                new_k = k.split(':')
                new_tokens.append(new_k[0])
            return new_tokens
worker_ids = []
text_number = 0
def answer_conversion(answer):
    if answer == "false":
        return 'no'
    else:
        return 'yes'
token_id = 0
for text in texts:
    text_number += 1
    new_data = pd.DataFrame(columns=data_top)
    for index, row in data.iterrows():
        if row['text'] == text:
            worker_id = row['workerid']
            if worker_id in approved_workerids:
                tokens = row['answer']
                new_answer = tokens.split(',\\"')
                new_answer2 = []
                for j in new_answer:
                    newj = j.replace('\\"', '')
                    newj = newj.replace('"{', '')
                    newj = newj.replace('}"', '')
                    new_answer2.append(newj.strip())
                new_tokens = tokenization(text)
                token_number = 0
                for token in new_tokens:
                    if token != 'none':
                        for k in new_answer2:
                            new_k = k.split(':')
                            if token == new_k[0]:
                                answer = new_k[1]
                                answer = answer_conversion(answer)
                                token_number += 1
                                token_number2 = str(token_number) + '_' + str(row['id'])
                                for ann_date_time in list_of_anotators_and_submissiontime:
                                    if ann_date_time[0] == worker_id:
                                        started_time = ann_date_time[1]
                                        completed_time = ann_date_time[2]
                                        date = ann_date_time[3]
                                        started_time = started_time[1]
                                        started_time = started_time.split('.')
                                        started_time = started_time[0]
                                        completed_time = completed_time.split('.')
                                        completed_time = completed_time[0]
                                        start = date + ' ' + started_time
                                        submission = date + ' ' + completed_time
                                        token_id += 1
                                        label_id = row['label'] + ' ' + token_number2
                                        answer_data = [[row['filename'], worker_id, start, answer, row['dataset'], token, token, label_id, token_id, token_number2, submission]]
                                        answer_df = pd.DataFrame(answer_data, columns=data_top)
                                        new_data = new_data.append(answer_df)
    list_of_dataframes.append(new_data)
import crowdtruth
from crowdtruth.configuration import DefaultConfig
class TestConfig(DefaultConfig):
    inputColumns = ['filename', 'dataset', 'text', 'label']
    outputColumns = ["selected_answer"]

    # processing of a closed task
    open_ended_task = False
    annotation_vector = ["yes", "no"]

    def processJudgments(self, judgments):
        # pre-process output to match the values in annotation_vector
        for col in self.outputColumns:
            # transform to lowercase
            judgments[col] = judgments[col].apply(lambda x: str(x).lower())
        return judgments
average_text_uqs = 0
initial_targeting_annotation_score = 0
initial_non_targeting_annotation_score = 0
targeting_examples = 0
non_targeting_examples = 0
uqs_count = 0
text_count = 0
uqs_list = []
initial_targeting_annotation_score_list = []
initial_non_targeting_annotation_score_list = []
def standard_deviation (mean, l):
    variance = sum([((x - mean) ** 2) for x in l]) / len(l)
    res = variance ** 0.5
    return res
count_row = 0
import re
def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)
for text in list_of_dataframes:
    text_count += 1
    text.to_csv('loop file.csv', sep=',')
    data, config = crowdtruth.load(
        file='loop file.csv',
        config=TestConfig()
    )
    results = crowdtruth.run(data, config)
    results["units"].to_csv(
        'uqs_example.csv')
    units = results["units"]
    uqss = units['uqs']
    unit_annotation_score_initials = units['unit_annotation_score_initial']
    input_labels = units['input.label']
    tokens = units['input.text']
    tokens_list = []
    for t in tokens:
        tokens_list.append(t)
    tokens_set = set(tokens_list)
    sorted_tokens = sorted_nicely(tokens_set)
    for token2 in sorted_tokens:
        for units_index in range(len(units)):
            token = tokens[units_index]
            if token2 == token:
                count_row += 1
                uqs = uqss[units_index]
                unit_annotation_score_initial = unit_annotation_score_initials[units_index]
                yes_ratio = unit_annotation_score_initial['yes']
                no_ratio = unit_annotation_score_initial['no']
                input_label = input_labels[units_index]
                if yes_ratio < no_ratio:
                    given_label = 'non targeting'
                else:
                    if no_ratio < yes_ratio:
                        given_label = 'targeting'
                    else:
                        given_label = 'undecided'
                if uqs < 0.6:
                    final_label = 'undecided'
                else:
                    if given_label == 'targeting':
                        final_label = 'targeting'
                    else:
                        if given_label == 'non targeting':
                            final_label = 'non targeting'
                        else:
                            final_label = 'undecided'
                worksheet.write(count_row, 0, token)
                worksheet.write(count_row, 1, input_label)
                worksheet.write(count_row, 2, final_label)
                worksheet.write(count_row, 3, uqs)
workbook.close()












