import operator
import numpy as np
from scipy import spatial
from methods import read_pickle, read_csv, write_dict_to_csv


def get_id_to_questions(input_file):
    result = {}     # Dictionary where key is ID, value is list of questions
    input_data = read_csv(input_file, True)   # 2D array where first column is question, second column is question ID

    for row in input_data:
        current_id = int(row[1])
        if current_id not in result:
            result[current_id] = []

        result.get(current_id).append(row[0])

    return result


def get_questions_to_id(input_file):
    result = {}     # Dictionary where key is question, value is ID
    input_data = read_csv(input_file, True)

    for row in input_data:
        result[row[0]] = int(row[1])

    return result


def get_k_nearest_neighbor(test_question, training_questions, question_to_embedding, k, training_questions_to_id, distance_measurement):
    distance_dict = {}      # Dictionary where key is question and value is distance
    test_embedding = question_to_embedding[test_question]

    for training_question in training_questions:
        training_embedding = question_to_embedding.get(training_question)
        current_distance = 0

        if distance_measurement == 'Euclidean':
            current_distance = np.linalg.norm(list(np.subtract(test_embedding, training_embedding)))
        elif distance_measurement == 'Cosine':
            current_distance = spatial.distance.cosine(list(test_embedding), list(training_embedding))

        if current_distance is not 0:
            distance_dict[training_question] = current_distance
        else:
            print(f"Error, distance is 0 for question: {training_question}")
    
    sorted_distance_dict = sorted(distance_dict.items(), key=operator.itemgetter(1))
    results = []
    ids = []

    for i in range(len(sorted_distance_dict)):
        if len(results) < k:
            current_prediction = sorted_distance_dict[i][0]
            current_id = training_questions_to_id[current_prediction]

            if current_id not in ids:
                results.append(current_prediction)
                ids.append(current_id)
        else:
            break

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
            predicted_neighbors = get_k_nearest_neighbor(test_question, training_questions, question_to_embedding, k, training_questions_to_id, distance_measurement = 'Cosine')
            test_to_predictions[test_question] = predicted_neighbors
            # print(f"Test: {test_question} | Predictions: {predicted_neighbors}")

            if is_correct(training_questions_to_id, predicted_neighbors, question_id):
                current_correct += 1

            current_total += 1

        id_accuracy = 1.0*current_correct/current_total

        accuracies_by_id.append(id_accuracy)

    write_dict_to_csv('predictions.csv', test_to_predictions)

    return round(np.mean(accuracies_by_id), 3)


#           MAIN            #

for input_test_set in ['dataset/testA.csv', 'dataset/testB.csv']:
    print(input_test_set)
    for n in [1, 3, 5]:
        print(get_accuracy(input_test_set, 'dataset/question_embeddings.pickle', 'dataset/train3.csv', n))