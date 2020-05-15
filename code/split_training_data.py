import random
from methods import read_csv, write_dict_to_csv

def get_questions(input_file):
    result = {}     # Dictionary where key is ID, value is list of questions
    input_data = read_csv(input_file)   # 2D array where first column is question, second column is question ID

    for row in input_data:
        if row[1] not in result:
            result[row[1]] = []

        result.get(row[1]).append(row[0])

    return result


def get_new_dataset(input_data, num_questions):
    result = {}     # Dictionary where key is question, value is question ID

    for question_id in input_data.keys():
        current_questions = input_data.get(question_id)
        random.shuffle(current_questions)

        for question in current_questions[:num_questions]:
            result[question] = question_id

    return result


#           MAIN            #
input_data = get_questions('dataset/train3.csv')
output_data = get_new_dataset(input_data, 1)
write_dict_to_csv('train1.csv', output_data)