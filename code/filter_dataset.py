import json
from methods import save_to_pickle, write_dict_to_csv, add_column, write_list_to_csv

def read_json(input_path):
    file = open(input_path,)

    result = {}     #type i dictionary with key = question and value = answer
    data = json.load(file)
    values =  list(data.values())

    for i in range(len(values)):
        for m in range(len(values[i])):
            current = values[i][m]     #type = dictionary with 1 key - "paragraphs"

            current_values = list(current.values())[0][0]   #type = dictionary with 3 keys - "qas", "context", "document_id"
            current_data = current_values.get('qas')    #type = list of dictionaries

            for j in range(len(current_data)):
                current_qa = current_data[j]      #type = dictionary with 4 keys - "question", "id", "answers", "is_impossible"

                result[current_qa.get('question')] = current_qa.get('answers')
    
    print(f"Obtained {len(result)} questions from full dataset.")
    return result


def read_txt(input_file):
    result = []

    all_lines = open(input_file, 'r').readlines()

    for line in all_lines:
        if '?' in list(line):   # Only save the questions
            result.append(line[:-1])
    
    return result


def contains_keyword(question, acceptable_keywords):
    for keyword in acceptable_keywords:
        if keyword.lower() in question.lower():
            return True

    return False


def filter_dictionary(input_dictionary, acceptable_keywords):
    result = {}
    
    all_questions = input_dictionary.keys()
    filtered_questions = []
    deleted_questions = []

    # Loop through questions and only keep questions related to COVID
    for question in all_questions:
        if contains_keyword(question, acceptable_keywords) is True:
            filtered_questions.append(question)
        else:
            deleted_questions.append(question)

    filtered_questions = set(filtered_questions)

    # Remake dictionary with filtered values
    for question in filtered_questions:
        result[question] = input_dictionary.get(question)[0].get('text')

    print(f"Filtered questions for a new dataset of size: {len(result)}.")
    return result


########## MAIN ##########
acceptable_keywords = ['COVID', 'coronavirus', 'nCOV' 'SARS-COV-2', 'COV']      # List of acceptable keywords - different capitalization permutations need not be included
input_path_json = 'data/original_qanda.json'     # Path to json file
input_path_txt = 'data/PDFs/Quora.txt'

# full_qa_dataset = read_json(input_path_json)
# filtered_qa_dataset = filter_dictionary(full_qa_dataset, acceptable_keywords)
# write_dict_to_csv('full_dataset.csv', filtered_qa_dataset)
# add_column('new_data1.csv', 'data/Yahoo_Dataset.csv', '-')
# add_column('new_data2.csv', 'new_data1.csv', 'Yahoo Autocomplete')
# add_column('new_data3.csv', 'new_data2.csv', '04 May 2020')

dataset = read_txt(input_path_txt)
write_list_to_csv('data1.csv', dataset)
add_column('data2.csv', 'data1.csv', '-')
add_column('data3.csv', 'data2.csv', 'Quora')
add_column('Quora_Dataset.csv', 'data3.csv', '07 May 2020')
##########################