from methods import read_csv, write_dict_to_csv

def get_id_to_category(input_file):
    input_data = read_csv(input_file, True)

    id_to_category = {}     # Dict where key is ID and value is category

    for row in input_data:
        id_to_category[row[1]] = row[0]

    return id_to_category

def compile_turk_dataset(input_file, category_file):
    input_data = read_csv(input_file, False)
    id_to_category = get_id_to_category(category_file)

    result = {}

    for row in input_data:
        question = row[0]
        question_id = row[1]
        category = id_to_category[question_id]
        result[question] = category

    write_dict_to_csv('turk_dataset.csv', result)


# MAIN #
compile_turk_dataset(input_file = 'dataset/train3.csv', category_file = 'data/final_master_dataset.csv')