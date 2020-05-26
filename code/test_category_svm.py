# Tests BERT embeddings with an SVM model

from methods import read_pickle, read_csv, write_dict_to_csv
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score


def get_embedding_data(input_file, category_to_num, question_to_embedding):
    input_data = read_csv(input_file, False)

    embeddings = []
    labels = []

    for row in input_data:
        if row[1] == '':
            continue
        else:
            embedding = question_to_embedding[row[0]]
            category_number = category_to_num[row[1]]
            embeddings.append(embedding)
            labels.append(category_number)

    return np.asarray(embeddings), np.asarray(labels)


def check_predictions(classifier, embeddings, ground_truth):
    predictions = classifier.predict(embeddings)

    return accuracy_score(ground_truth, predictions)



#       MAIN      #
category_to_num = {'Transmission': 0,
                   'Prevention': 1,
                   'Societal Effects': 2,
                   'Societal Response': 3,
                   'Reporting': 4,
                   'Origin': 5,
                   'Treatment': 6,
                   'Testing': 7,
                   'Comparison': 8,
                   'Individual Response': 9,
                   'Economic Effects': 10,
                   'Speculation': 11,
                   'Having COVID': 12,
                   'Nomenclature': 13,
                   'Symptoms': 14}
question_to_embedding = read_pickle('dataset_categories/augmented_question_embeddings.pickle')

train_x, train_y = get_embedding_data('dataset_categories/train20_augmented.csv', category_to_num, question_to_embedding)
testA_x, testA_y = get_embedding_data('dataset_categories/testA.csv', category_to_num, question_to_embedding)
testB_x, testB_y = get_embedding_data('dataset_categories/testB.csv', category_to_num, question_to_embedding)

classifier = svm.SVC()
classifier.fit(train_x, train_y)

print(f'Real Questions: {round(check_predictions(classifier, testA_x, testA_y), 3)}')
print(f'Generated Questions: {round(check_predictions(classifier, testB_x, testB_y), 3)}')