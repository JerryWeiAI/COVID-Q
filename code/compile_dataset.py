import csv
import operator
from methods import read_tsv, clean_line, read_csv

def compile_all_questions(input_data, master_dictionary, column_to_source, output_file, column_to_nice_source, id_to_category):
    # Start reading file
    with open(output_file, 'w', newline = '', encoding='UTF-8') as out_file:
        writer = csv.writer(out_file, dialect= 'excel', delimiter = ',')
        writer.writerow(['Category', 'Question ID', 'Question', 'Source', 'Answers'])

        id_to_questions = {}    # Dict where key = question ID and value = (dictionary where key = question, value = source)
        id_to_answers = {}      # Dict where key = question ID and value = list of answers
        id_to_num_questions = {}    # Dict where key = quesiton ID and value = number of matched questions

        # Same as iterating through each unique question ID
        for row in input_data[1:]:
            answers = []
            questions_to_source = {}

            for i in range(1, len(row)):
                if row[i] is '':
                    continue

                current_questions = set(clean_line(row[i]).split(', '))

                for each in current_questions:
                    source_dictionary = master_dictionary.get(i)
                    questions_to_source[each] = column_to_nice_source.get(i)
                    
                    if each in source_dictionary:
                        if source_dictionary.get(each) not in ['-', '', ' ']:
                            answers.append(source_dictionary.get(each))
                    elif i is not 1:    # Debugging for questions that can't be found in source dictionary
                        print(f'{each} from {column_to_source.get(i)} and {i} and Question ID {question_id}')

            question_id = row[0]
            id_to_questions[question_id] = questions_to_source
            id_to_answers[question_id] = answers
            id_to_num_questions[question_id] = len(list(questions_to_source.keys()))

        sorted_by_frequency = sorted(id_to_num_questions.items(), key=operator.itemgetter(1), reverse = True)

        for question_id, _ in sorted_by_frequency:
            for question in id_to_questions[question_id].keys():
                # Write out line
                writer.writerow([id_to_category[question_id],question_id, question, id_to_questions[question_id][question], clean_line(str(id_to_answers[question_id]).strip('[]'))])

            # writer.writerow([])


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
            

def get_id_to_category(input_file):
    input_data = read_csv(input_file)

    id_to_category = {}     # Dict where key is ID and value is category

    for row in input_data:
        id_to_category[row[1]] = row[0]

    return id_to_category


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
                    13: 'data/TSVs/Quora_Dataset.tsv',
                    14: 'data/TSVs/Generated_Questions.tsv'}
column_to_nice_source = {1: 'Google Search',
                         2: 'John Hopkins University',
                         3: 'Illinois Department of Public Health',
                         4: 'United Nations',
                         5: 'Food and Drug Administration',
                         6: 'Cable News Network',
                         7: 'Center for Disease Control', 
                         8: 'GitHub.com/deepset-ai/COVID-QA',
                         9: 'Washington DC Area Television Station',
                         10: 'Bing Search',
                         11: 'Yahoo Search',
                         12: 'Yahoo Answers',
                         13: 'Quora',
                         14: 'Author Generated'}

master_dictionary = compile_all_dictionary(column_to_source)
id_to_category = get_id_to_category('data/final_master_dataset.csv')
compile_all_questions(read_tsv(input_file), master_dictionary, column_to_source, output_file, column_to_nice_source, id_to_category)