
import pandas as pd
sentences = []
sentence = []
df = pd.read_excel ('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_ UQS Threshold 60.xlsx', header=[0])
#df = pd.read_excel ('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_ UQS Threshold 50.xlsx', header=[0])
#df = pd.read_excel ('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_ UQS Threshold 70.xlsx', header=[0])
for index, row in df.iterrows():
    token = row['Token'].split()
    if token[0] != '1-':
        token_label = (token[1], row['Assigned Label'])
        sentence.append(token_label)
    else:
        sentences.append(sentence)
        sentence = []
        token_label = (token[1], row['Assigned Label'])
        sentence.append(token_label)
sentences.append(sentence)
sentences = [ele for ele in sentences if ele != []]
all_spans = []
for sentence in sentences:
    spans = []
    span = []
    for token in range(len(sentence)):
        sentence_token = sentence[token]
        t = sentence_token[1]

        word = sentence_token[0]
        if t == 'targeting':
            if token != 0:
                previous_sentence_token = sentence[token - 1]
                p = previous_sentence_token[1]
                if p == 'targeting':
                    word_postition = (token, word)
                    span.append(word_postition)
                else:
                    word_postition = (token, word)
                    span.append(word_postition)
            else:
                word_postition = (token, word)
                span.append(word_postition)
        else:
            word_postition = (token, word)
            spans.append(span)
            span = []
    spans.append(span)
    spans = [ele for ele in spans if ele != []]
    all_spans.append(spans)

labels = []
for s in range(len(sentences)):
    sentence = sentences[s]
    position_tokens = all_spans[s]
    word_index = -1

    for word_label in sentence:
        found = False
        word_index += 1
        if word_label[1] == 'non-targeting':
            label = '0'
            labels.append(label)
            found = True
        else:
            if found == False:
                for position_token in position_tokens:
                    if found == False:
                        for p_t in position_token:
                            if found == False:
                                index = position_token.index(p_t)
                                if p_t[0] == word_index:
                                    if index == 0:
                                        label = '1'
                                        labels.append(label)
                                        found = True
                                    else:
                                        label = '2'
                                        labels.append(label)
                                        found = True
                            else:
                                break
                    else:
                        break
            else:
                break



import xlsxwriter
workbook = xlsxwriter.Workbook('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_IOB labels_ UQS Threshold 60.xlsx')
#workbook = xlsxwriter.Workbook('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_IOB labels_ UQS Threshold 50.xlsx')
#workbook = xlsxwriter.Workbook('/annotation results/batches 1 - 120/HateXplain_Target Span Detection_Assigned Labels (Batches 1 - 120)_IOB labels_ UQS Threshold 70.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_column('A1', labels)
workbook.close()



