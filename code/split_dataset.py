import csv
import random
from methods import read_csv, write_dict_to_csv

def split_dataset(master_data):
    # Dictionary where key is question ID, value is [real questions that match that ID, generated questions that match that ID]
    id_to_questions = {}

    # Output dictionaries where key is question, value is ID
    train_dict = {}
    testA_dict = {}
    testB_dict = {}    
    
    # Count number of questions for each ID
    for row in master_data:
        question_id = row[1]
        question = row[2]
        index = 0

        if row[3] == "Author Generated":
            index = 1

        if question_id in id_to_questions.keys():
            id_to_questions.get(question_id)[index].append(question)
        else:
            id_to_questions[question_id] = [[], []]
            id_to_questions.get(question_id)[index].append(question)

    # Split data
    counter = 0
    for current_id in id_to_questions.keys():
        real_questions = id_to_questions.get(current_id)[0]
        generated_questions = id_to_questions.get(current_id)[1]

        if len(real_questions) >= 4:    #If there are at least 4 questions
            random.shuffle(real_questions)
            
            for question in real_questions[:3]:
                train_dict[question] = current_id
            
            for question in real_questions[3:]:
                testA_dict[question] = current_id

            for question in generated_questions:
                testB_dict[question] = current_id

            counter += 1

    print(f"{counter} distinct question IDs")

    return [train_dict, testA_dict, testB_dict]

#           MAIN            #
master_data = read_csv('data/final_master_dataset.csv', True)
output_names = 'train3.csv', 'testA.csv', 'testB.csv'

sub_datasets = split_dataset(master_data)

for i in range(3):
    write_dict_to_csv(output_names[i], sub_datasets[i])