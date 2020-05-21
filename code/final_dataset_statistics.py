from methods import read_csv
import operator

def compute_statistics(input_csv):
    input_data = read_csv(input_csv, True)

    result = {}     # Dictionary where key = category and value = [list of IDs, list of Questions]

    for row in input_data:
        category = row[0].split(' - ')[0]
        question_id = row[1]
        question = row[2]

        if category in result.keys():
            result.get(category)[0].append(question_id)
            result.get(category)[1].append(question)
        else:
            result[category] = [[], []]
            result.get(category)[0].append(question_id)
            result.get(category)[1].append(question)
            
    category_to_numQuestions = {}   # Dict where key = category and value = number of unique questions
    category_to_numClasses = {}

    for category in result.keys():
        category_to_numQuestions[category] = len(set(result.get(category)[1]))
        category_to_numClasses[category] = len(set(result.get(category)[0]))

    category_to_numQuestions = sorted(category_to_numQuestions.items(), key=operator.itemgetter(1), reverse = True)

    for i in range(len(category_to_numQuestions)):
        category = category_to_numQuestions[i][0]
        print(category, category_to_numQuestions[i][1], category_to_numClasses[category])

    return result


#       MAIN        #
compute_statistics('data/final_master_dataset.csv')