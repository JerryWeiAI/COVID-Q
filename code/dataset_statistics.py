import csv
from methods import read_tsv


def calculate_source_statistics(input_path, master_dictionary, column_to_source):
    # Formatted as key = source ID; value = [num questions, num answers, num questions with match]
    result = {1: [0, 0, 0],
              2: [0, 0, 0],
              3: [0, 0, 0],
              4: [0, 0, 0],
              5: [0, 0, 0],
              6: [0, 0, 0],
              7: [0, 0, 0],
              8: [0, 0, 0],
              9: [0, 0, 0],
              10: [0, 0, 0],
              11: [0, 0, 0],
              12: [0, 0, 0],
              13: [0, 0, 0],
              14: [0, 0, 0]}

    num_questions_dict = {}  # Formatted as key = number; value = number of question IDs that have that many matched questions
    very_common_questions = {}  # Formatted as key = sample question, value = number of matched questions inclusive
    to_be_annotated_ids = []  # List of questions IDs with 2, 3, 4, or 5 matching questions
    num_questions_w_sources = 0       # Number of question IDs with questions from at least 2 non-official sources
    num_answered_questions = 0      # Number of question IDs with questions from at least 2 non-official sources that are answered 

    input_data = read_tsv(input_path)

    # Record dataset statistics
    for row in input_data[1:]:
        # Count number of questions associated with this question ID
        all_questions = []      # List of questions associated with this question ID
        num_sources = 0         # Number of sources with a question in this question ID
        for i in range(1, len(row) - 1):    # length - 1 to not count author generated questions
            if row[i] is '':
                continue

            if i not in [2, 3, 4, 5, 6, 7, 9]:
                num_sources += 1

            current_questions = (set)(row[i].split(', '))
            for question in current_questions:
                all_questions.append(question)

        num_questions = len(set(all_questions))

        if num_questions not in num_questions_dict.keys():
            num_questions_dict[num_questions] = 1
        else:
            num_questions_dict[num_questions] = num_questions_dict.get(num_questions) + 1

        if num_questions > 10:
            very_common_questions[list(current_questions)[0]] = num_questions
        elif num_questions in [4, 5]:
            to_be_annotated_ids.append(row[0])

        answered = False

        # Count each question
        for i in range(1, len(row)):
            if row[i] is '':
                continue

            current_questions = set(row[i].split(', '))

            for each in current_questions:

                source_dictionary = master_dictionary.get(i)
                has_answer = False

                if each in source_dictionary:
                    if source_dictionary.get(each) is not '-' and source_dictionary.get(each) is not ' ':
                        has_answer = True
                        answered = True
                
                # Update values
                result.get(i)[0] += 1
                if has_answer is True:
                    result.get(i)[1] += 1
                if num_questions > 1:
                    result.get(i)[2] += 1

        if num_sources >= 2:
            num_questions_w_sources += 1
            
            if answered is True:
                num_answered_questions += 1
            else:
                if len(all_questions) > 8:
                    print(all_questions)

    # Print results
    # for key in result.keys():
    #     print(f"Source {column_to_source.get(key)} with {result.get(key)[0]} questions and {result.get(key)[1]} answers has {result.get(key)[2]} matched questions")

    # print("------------------------------------------------------------------------------")

    # for key in sorted(num_questions_dict.keys()):
    #     print(f"{num_questions_dict.get(key)} questions IDs have {key} questions")

    # for key in sorted(num_questions_dict.keys()):
    #     print(f"({key}, {num_questions_dict.get(key)})")

    # print("------------------------------------------------------------------------------")

    # print(very_common_questions)
    # print(str(len(very_common_questions)))

    # print(to_be_annotated_ids)
    # print(str(len(to_be_annotated_ids)))

    print(num_answered_questions, num_questions_w_sources)

    return result


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

master_dictionary = compile_all_dictionary(column_to_source)
calculate_source_statistics(input_file, master_dictionary, column_to_source)