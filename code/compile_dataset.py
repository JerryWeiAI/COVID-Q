import csv
from methods import clean_line, read_tsv

x = 0

def compile_all_questions(input_data, master_dictionary, column_to_source, output_file):
    # Start reading file
    with open(output_file, 'w', newline = '', encoding='UTF-8') as out_file:
        writer = csv.writer(out_file, dialect= 'excel', delimiter = ',')
        writer.writerow(['Question ID', 'Question', 'Source', 'Answers'])

        # Same as iterating through each unique question ID
        for row in input_data[1:]:
            answers = []
            questions_to_source = {}

            for i in range(1, len(row)):
                if row[i] is '':
                    continue

                current_questions = set(row[i].split(', ')) 

                for each in current_questions:
                    source_dictionary = master_dictionary.get(i)
                    questions_to_source[each] = column_to_source.get(i)
                    
                    if each in source_dictionary:
                        if source_dictionary.get(each) is not '-' and source_dictionary.get(each) is not ' ':
                            answers.append(source_dictionary.get(each))
                    elif i is not 1:
                        print(f'{each} from {column_to_source.get(i)} and {i}')

            for each in questions_to_source.keys():
                # Write out line
                writer.writerow([row[0], each, questions_to_source.get(each), str(answers).strip('[]')])


def read_sub_dataset(input_file):
    result = {}     # Dictionary where key = question and value = answer

    input_data = read_tsv(input_file)

    for row in input_data:
        # print(row)
        result[row[0]] = row[1]

    return result             


def compile_all_dictionary(column_to_source):
    result = {}     # Dictionary where key = column number and value = dictionary of (question: answer) for corresponding source

    for key in column_to_source.keys():
        current_source_qanda = read_sub_dataset(column_to_source.get(key))

        result[key] = current_source_qanda

    return result
            


#           MAIN            #
input_file = 'data/TSVs/All_Matched_Questions.tsv'
output_file = 'data/master_dataset.csv'
column_to_source = {1: 'data/TSVs/KeywordTool_Dataset.tsv',
                    2: 'data/TSVs/John-Hopkins_Dataset.tsv',
                    3: 'data/TSVs/IDPH_Dataset.tsv',
                    4: 'data/TSVs/UN_Dataset.tsv',
                    5: 'data/TSVs/FDA_Dataset.tsv',
                    6: 'data/TSVs/CNN_Dataset.tsv',
                    7: 'data/TSVs/CDC_Dataset.tsv',
                    8: 'data/TSVs/COVID-QA_Dataset.tsv',
                    9: 'data/TSVs/WJLA_Dataset.tsv',
                    10: 'data/TSVs/Bing_Dataset.tsv',
                    11: 'data/TSVs/Yahoo_Dataset.tsv',
                    12: 'data/TSVs/Yahoo-Answers_Dataset.tsv',
                    13: 'data/TSVs/Quora_Dataset.tsv'}

master_dictionary = compile_all_dictionary(column_to_source)
compile_all_questions(read_tsv(input_file), master_dictionary, column_to_source, output_file)