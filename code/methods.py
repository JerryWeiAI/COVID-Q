import csv
import pickle
import re

# Reads in a pickle as a dictionary
def read_pickle(input_path):
    return pickle.load(open(input_path, 'rb'))


# Returns 2D representation of a csv file
def read_csv(input_path, skip_header):
    result = []

    with open(input_path, 'r', encoding = 'UTF-8') as file:
        reader = csv.reader(file, delimiter = ',')

        if skip_header is True:
            next(reader, None)

        for row in reader:
            result.append(row)

    return result


# Input file must be a list
def write_list_to_csv(output_path, input_file):
    with open(output_path, 'w', newline = '') as file:
        writer = csv.writer(file)
        for each in input_file:
            print(each)
            writer.writerow([each])


# Input file must be a dictionary
def write_dict_to_csv(output_path, input_file):
    with open(output_path, 'w', newline = '') as file:
        writer = csv.writer(file)
        for key in input_file.keys():
            writer.writerow([key, input_file.get(key)])


# Adds a column where everything says to_be_added
def add_column(output_path, input_csv_file, to_be_added):
    with open(input_csv_file, newline = '') as in_file:
        with open(output_path, 'w', newline = '') as out_file:
            reader = csv.reader(in_file)
            writer = csv.writer(out_file)

            for row in reader:
                row.append(to_be_added)
                writer.writerow(row)


# Returns 2D array representation of a TSV file
def read_tsv(input_file):
    result = []
    lines = open(input_file, 'r', encoding = 'UTF-8').readlines()
    
    for line in lines:
        line = clean_line(line)

        parts = line[:-1].split('\t')
        result.append(parts)

    return result


# Removes weird characters from a string
def clean_line(string):
    string = string.replace(u'\xa0', ' ')
    string = string.replace(u'"', '').replace('“', '').replace('”', '')
    string = string.replace("‘", '').replace("’", '').replace("'", '')
    string = string.replace('-', ' ').replace('–', ' ')
    string = string.replace(":", '').replace('=', '')
    string = string.lower() 

    return string


# Saves a dictionary out to a pickle file
def save_to_pickle(input_dict, output_filename):
    with open(output_filename, 'wb') as handle:
        pickle.dump(input_dict, handle, protocol = 2)
    
    print("Successfully saved to pickle.")