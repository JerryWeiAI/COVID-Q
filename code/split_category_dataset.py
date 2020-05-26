import random
from methods import read_csv, write_dict_to_csv


def split_dataset_category(input_file):
    input_data = read_csv(input_file, True)

    category_to_questions = {}      # Dict where key = category, value = [list of real questions in that category, list of generated questions in that category]

     # Output dictionaries where key is question, value is category
    train_dict = {}
    testA_dict = {}
    testB_dict = {} 

    # Add questions to categories
    for row in input_data:
        category = row[0].split(' - ')[0]
        question = row[2]
        source = row[3]

        if category in category_to_questions.keys():
            if source == 'Author Generated':
                category_to_questions.get(category)[1].append(question)
            else:
                category_to_questions.get(category)[0].append(question)
        else:
            category_to_questions[category] = [[], []]

            if source == 'Author Generated':
                category_to_questions.get(category)[1].append(question)
            else:
                category_to_questions.get(category)[0].append(question)

    for category in category_to_questions.keys():
        if category == '' or category == 'Other':
            continue

        real_questions = category_to_questions.get(category)[0]
        generated_questions = category_to_questions.get(category)[1]

        print(category, len(real_questions))

        random.shuffle(real_questions)
        random.shuffle(generated_questions)

        for question in generated_questions:
            testB_dict[question] = category
 
        counter = 0
        for i in range(len(real_questions)):
            question = real_questions[i]

            if counter < 20:
                if question not in train_dict:
                    counter += 1
                    train_dict[question] = category
            else:
                if question not in testA_dict:
                    counter += 1
                    testA_dict[question] = category

    return [train_dict, testA_dict, testB_dict]


#       MAIN        #
output_names = 'train20.csv', 'testA.csv', 'testB.csv'
input_file = 'data/final_master_dataset.csv'

sub_datasets = split_dataset_category(input_file)

for i in range(3):
    write_dict_to_csv(output_names[i], sub_datasets[i])