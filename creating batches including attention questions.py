import pandas as pd
from pathlib import Path
df = pd.read_csv ('WholeDataSetHateXplainTargetingSortedTargets_EqualTargets 1.csv', header=[0], on_bad_lines='skip', sep = ';')
#df = pd.read_csv ('WholeDataSetHateXplainTargetingSortedTargets_EqualTargets 2.csv', header=[0], on_bad_lines='skip', sep = ';')
count = 0
column_names = ["id", "dataset", "text", 'tokens', 'label']
new_df = pd.DataFrame(columns = column_names)
df2 = pd.read_excel('attention check sentences (HateXplain targeting).xlsx', header=[0])
list_of_attention_sentences = df2['sentence'].to_list()
for i in range(len(list_of_attention_sentences)):
    list_of_attention_sentences[i] = list_of_attention_sentences[i].lower()
new_df2 = pd.DataFrame(columns = column_names)
counter = 0
from nltk.tokenize import word_tokenize
import string
for i in list_of_attention_sentences:
    counter += 1
    id = 'attention_' + str(counter)
    dataset = 'attention check sentences (HateXplain targeting)'
    text = i
    new_string = text.translate(str.maketrans('', '', string.punctuation))
    new_string = word_tokenize(new_string)
    sample_len = len(new_string)
    sentence = ''
    tokens = ''
    count_len = 0
    count_word = 0
    for word in new_string:
        count_word += 1
        count_len += 1
        sentence += word
        new_word = str(count_word) + "- " + word
        tokens += new_word
        if count_len != sample_len:
            tokens += ', '
            sentence += ' '
    text = sentence
    label = 'offensive'
    dataframe_data = [[id, dataset, text, tokens, label]]
    df3 = pd.DataFrame(dataframe_data, columns=column_names)
    new_df2 = new_df2.append(df3, ignore_index=True)
root_directpry = '/annotation batches/'
def file_creation(dataframe, batch_number):
    filepath = Path(root_directpry + 'batch_' + str(batch_number)+ '.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(filepath, sep = ';')
batch_number = 113
count_row = 0
for index, row in df.iterrows():
    count_row += 1
    count += 1
    if count % 29 == 0:
        new_df.loc[count] = list(row)
        random_df = new_df2.sample(n=1)
        new_df = new_df.append(random_df)
        file_creation(new_df, batch_number)
        batch_number += 1
        new_df = pd.DataFrame(columns=column_names)
    else:
        new_df.loc[count] = list(row)




