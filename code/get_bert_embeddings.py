import torch
import numpy as np
import csv
from transformers import BertModel, BertTokenizer
from methods import clean_line, save_to_pickle, read_csv, read_pickle

# Encode text
def get_embedding(input_string, tokenizer, model):
    input_ids = torch.tensor([tokenizer.encode(input_string, add_special_tokens = True)])  # Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for each model.
    with torch.no_grad():
        last_hidden_states = model(input_ids)[0].numpy()  # Models outputs are now tuples
        # last_hidden_states = last_hidden_states[:, 0, :]
        last_hidden_states = np.mean(last_hidden_states, axis = 1)
        # last_hidden_states = np.amax(last_hidden_states, axis = 1)
        last_hidden_states = last_hidden_states.flatten()
        return last_hidden_states.tolist()


# Gets all encodings given an input csv
def get_all_embeddings(input_csv, tokenizer, model):
    result = {}     # Dictionary where key = question and value = bert embedding for that question

    reader = read_csv(input_csv, True)

    for row in reader:
        question = row[2]
        embedding = get_embedding(question, tokenizer, model)
        question = ''.join([i if ord(i) < 128 else ' ' for i in question])

        result[question] = embedding

    return result


def combine_with_augmented_dataset(original_pickle_path, new_pickle_path, augmented_dataset_path, tokenizer, model):
    original_data = read_pickle(original_pickle_path)
    augmented_data = read_csv(augmented_dataset_path, skip_header = False)

    for row in augmented_data:
        question = row[0]
        embedding = get_embedding(question, tokenizer, model)
        question = ''.join([i if ord(i) < 128 else ' ' for i in question])

        original_data[question] = embedding

    save_to_pickle(original_data, new_pickle_path)

    return original_data


#           MAIN            #
model_class = BertModel
tokenizer_class = BertTokenizer
pretrained_weights = 'bert-base-uncased'
input_csv = 'data/final_master_dataset.csv'

# Load pretrained model/tokenizer
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)

# all_embeddings = get_all_embeddings(input_csv, tokenizer, model)
# save_to_pickle(all_embeddings, 'question_embeddings_max.pickle')

combine_with_augmented_dataset('dataset_categories/question_embeddings_pooled.pickle', 'augmented_question_embeddings.pickle', 'dataset_categories/train20_augmented.csv', tokenizer, model)