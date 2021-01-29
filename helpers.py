import os
import csv


def dict_to_list_mapper(x_dict: dict, y_list: list):
    output = [None] * len(y_list)
    for key in x_dict:
        val = x_dict[key]
        idx = y_list.index(key)
        output[idx] = val
    return output

def check_versions(dir_path, file_name):
    if os.path.exists(os.path.join(dir_path, file_name)):
        print(f'The File {file_name} Already Exists! Creating a new version...')
        i = 2
        new_file_name = file_name
        while os.path.exists(os.path.join(dir_path, new_file_name)):
            new_file_name = f'v{i}_{file_name}'
            i += 1
        file_name = new_file_name
        print(f'New version for file: {file_name}')

    return file_name


def make_dir(dir_chain: list):
    destination_dir = './'
    for folder in dir_chain:
        destination_dir = os.path.join(destination_dir, folder)
        if not os.path.isdir(destination_dir):
            os.mkdir(destination_dir)

    return destination_dir


def make_csv(dir_chain: list, file_name: str, columns: list):

    destination_dir = make_dir(dir_chain)

    if not file_name.endswith('.csv'):
        file_name = f'{file_name}.csv'

    path = os.path.join(destination_dir, file_name)
    with open(path, 'w', newline='', encoding="utf-8") as csvout:
        writer = csv.writer(csvout, delimiter=',', quotechar='"')
        writer.writerow(columns)
        csvout.flush()

    return path


def get_num_processes(required_cores, max_cores=-1):
    total_cores = os.cpu_count()

    if max_cores == -1:
        return total_cores

    elif required_cores <= max_cores:
        return required_cores

    elif required_cores > max_cores:

        if max_cores <= total_cores:
            return max_cores
        else:
            raise OSError(f'The number of max cores to use {max_cores} exceeds the total availble cores {total_cores}'
                          f'on this machine')