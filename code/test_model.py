import operator
import numpy as np
from methods import read_pickle, read_csv, write_dict_to_csv


def get_id_to_questions(input_file):
    result = {}     # Dictionary where key is ID, value is list of questions
    input_data = read_csv(input_file)   # 2D array where first column is question, second column is question ID

    for row in input_data:
        current_id = int(row[1])
        if current_id not in result:
            result[current_id] = []

        result.get(current_id).append(row[0])

    return result


def get_questions_to_id(input_file):
    result = {}     # Dictionary where key is question, value is ID
    input_data = read_csv(input_file)

    for row in input_data:
        result[row[0]] = int(row[1])

    return result


def get_k_nearest_neighbor(test_question, training_questions, question_to_embedding, k):
    distance_dict = {}      # Dictionary where key is question and value is distance
    test_embedding = question_to_embedding.get(test_question)

    for training_question in training_questions:
        training_embedding = question_to_embedding.get(training_question)
        current_distance = np.linalg.norm(list(np.subtract(test_embedding, training_embedding)))

        distance_dict[training_question] = current_distance
    
    sorted_distance_dict = sorted(distance_dict.items(), key=operator.itemgetter(1))
    results = []

    for i in range(k):
        results.append(sorted_distance_dict[i][0])

    return results


def is_correct(training_questions_to_id, predicted_neighbors, question_id):
    for prediction in predicted_neighbors:
        if training_questions_to_id[prediction] is question_id:
            return True

    return False


def get_accuracy(test_question_to_id_path, embedding_path, training_question_to_id_path, k):
    question_to_embedding = read_pickle(embedding_path)
    test_id_to_questions = get_id_to_questions(test_question_to_id_path)
    training_questions_to_id = get_questions_to_id(training_question_to_id_path)
    training_questions = training_questions_to_id.keys()

    accuracies_by_id = []
    test_to_predictions = {}

    for question_id in test_id_to_questions.keys():
        current_correct = 0
        current_total = 0

        current_questions = test_id_to_questions.get(question_id)
        for test_question in current_questions:
            predicted_neighbors = get_k_nearest_neighbor(test_question, training_questions, question_to_embedding, k)
            test_to_predictions[test_question] = predicted_neighbors
            print(f"Test: {test_question} | Predictions: {predicted_neighbors}")

            if is_correct(training_questions_to_id, predicted_neighbors, question_id):
                current_correct += 1

            current_total += 1

        id_accuracy = 1.0*current_correct/current_total

        accuracies_by_id.append(id_accuracy)

    write_dict_to_csv('predictions.csv', test_to_predictions)

    return round(np.mean(accuracies_by_id), 3)


#           MAIN            #
print(get_accuracy('dataset/testB.csv', 'dataset/question_embeddings.pickle', 'dataset/train3.csv', 1))