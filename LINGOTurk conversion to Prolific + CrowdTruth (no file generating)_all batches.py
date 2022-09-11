
import pandas as pd
from pathlib import Path
row = 1
column = 0
import xlsxwriter
l = ['Batch', 'Average UQS', 'Average Targeting Initial Score', 'Average Non-targeting Initial Score', 'Standard Deviation of UQQSs', 'Standard Deviation of Targeting Initial Scores', 'Standard Deviation  of Non-targeting Initial Scores']
workbook = xlsxwriter.Workbook('Targeting_25 Batches_CrowdTruth.xlsx')
worksheet = workbook.add_worksheet()
for i in range(len(l)):
    worksheet.write(0, i, l[i])
import os
count_row = 0
from datetime import datetime
duplicate_rows = []
def month_to_number(month):
    datetime_object = datetime.strptime(month, "%b")
    month_number = datetime_object.month
    return str(month_number)
def month_extraction (time):
    time = time.split()
    date = time[0].split('/')
    month = date[1]
    return str(month)
def year_extraction (time):
    time = time.split()
    date = time[0].split('/')
    year = date[2]
    year = str(year)
    return str(year)
def remove_duplicates (data):
    for index, row in data.iterrows():
        for index2, row2 in data.iterrows():
            if index != index2:
                if row['workerid'] == row2['workerid']:
                    if row['id'] == row2['id']:
                        timestamp1 = row['timestamp']
                        timestamp2 = row2['timestamp']
                        if timestamp1 != timestamp2:
                            timestamp1 = timestamp1.replace("-", "/")
                            timestamp2 = timestamp2.replace("-", "/")
                            month1 = month_extraction(timestamp1)
                            month2 = month_extraction(timestamp2)
                            year1= year_extraction(timestamp1)
                            year2 = year_extraction(timestamp2)
                            month_number1 = month_to_number(month1)
                            month_number2 = month_to_number(month2)
                            timestamp1 = timestamp1.replace(month1, month_number1)
                            timestamp2 = timestamp2.replace(month2, month_number2)
                            timestamp1 = timestamp1.replace(year1, year1[2:])
                            timestamp2 = timestamp2.replace(year2, year2[2:])
                            timestamp1_obj = datetime.strptime(timestamp1, '%d/%m/%y %H:%M:%S')
                            timestamp2_obj = datetime.strptime(timestamp2, '%d/%m/%y %H:%M:%S')
                            if timestamp1_obj < timestamp2_obj:
                                if index not in duplicate_rows:
                                    duplicate_rows.append(index)
                            if timestamp2_obj < timestamp1_obj:
                                if index not in duplicate_rows:
                                    duplicate_rows.append(index2)
    data = data.drop(data.index[duplicate_rows])
    return data
rootdir = '/annotation results/'
for root, subdirectories, files in os.walk(rootdir):
    for subdirectory in subdirectories:
        count_row += 1
        new_subdirectory = os.path.join(root, subdirectory)
        results = 'results.csv'
        results_directory = os.path.join(new_subdirectory, results)
        demographic_data = 'demographic data.csv'
        demographic_data_directory = os.path.join(new_subdirectory, demographic_data)
        data = pd.read_csv(results_directory, header=[0])
        data = remove_duplicates(data)
        demographic_data = pd.read_csv(demographic_data_directory, header=[0])
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
        list_of_texts = data['text'].to_list()
        texts = list(set(list_of_texts))
        list_of_anotators_and_submissiontime = []
        approved_workerids = []
        for index, row in demographic_data.iterrows():
            if row['status'] == 'APPROVED':
                id = row['participant_id']
                submission_time_and_date = row['completed_date_time']
                submission_time = submission_time_and_date.split()
                date = submission_time[0]
                submission_time = submission_time[1]
                submission_time = submission_time.split('.')
                submission_time = submission_time[0]
                started_time_and_date = row['started_datetime']
                started_time_and_date = started_time_and_date.split()
                started_time = started_time_and_date[1]
                started_time = started_time.split('.')
                started_time = started_time[0]
                annotator_time = (id, started_time, submission_time, date)
                list_of_anotators_and_submissiontime.append(annotator_time)
                approved_workerids.append(id)
        list_of_dataframes = []
        count = 0


        def tokenization(text):
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
                                                start = date + ' ' + started_time
                                                submission = date + ' ' + completed_time
                                                token_id += 1
                                                answer_data = [
                                                    [row['filename'], worker_id, start, answer, row['dataset'], text,
                                                     token, row['label'], token_id, token_number2, submission]]
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


        def standard_deviation(mean, l):
            variance = sum([((x - mean) ** 2) for x in l]) / len(l)
            res = variance ** 0.5
            return res


        for text in list_of_dataframes:
            text_count += 1
            print(text_count)
            text.to_csv(
                'loop file.csv',
                sep=',')
            data, config = crowdtruth.load(
                file='loop file.csv',
                config=TestConfig()
            )
            results = crowdtruth.run(data, config)
            results["units"].to_csv(
                'uqs_example.csv')
            units = results["units"]
            uqs = units['uqs']
            unit_annotation_score_initial = units['unit_annotation_score_initial']
            for i in uqs:
                average_text_uqs += i
                uqs_count += 1
                uqs_list.append(i)
            for i in unit_annotation_score_initial:
                yes_ratio = i['yes']
                no_ratio = i['no']
                if yes_ratio > no_ratio:
                    initial_targeting_annotation_score += yes_ratio
                    targeting_examples += 1
                    initial_targeting_annotation_score_list.append(yes_ratio)
                if yes_ratio < no_ratio:
                    initial_non_targeting_annotation_score += no_ratio
                    non_targeting_examples += 1
                    initial_non_targeting_annotation_score_list.append(no_ratio)
        average_text_uqs = average_text_uqs / uqs_count
        average_targeting_initial_score = initial_targeting_annotation_score / targeting_examples
        average_non_targeting_initial_score = initial_non_targeting_annotation_score / non_targeting_examples
        res = standard_deviation(average_text_uqs, uqs_list)
        targeting_res = standard_deviation(average_targeting_initial_score, initial_targeting_annotation_score_list)
        non_targeting_res = standard_deviation(average_non_targeting_initial_score,
                                               initial_non_targeting_annotation_score_list)
        worksheet.write(count_row, 0, subdirectory)
        worksheet.write(count_row, 1, average_text_uqs)
        worksheet.write(count_row, 2, average_targeting_initial_score)
        worksheet.write(count_row, 3, average_non_targeting_initial_score)
        worksheet.write(count_row, 4, res)
        worksheet.write(count_row, 5, targeting_res)
        worksheet.write(count_row, 6, non_targeting_res)
workbook.close()
