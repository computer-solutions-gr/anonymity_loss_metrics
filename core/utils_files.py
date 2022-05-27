import os
import re

def run_scandir(dir):
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def get_files_in_directory(input_directory):
    subfolders, filepaths = run_scandir(input_directory)
    return filepaths


def get_parameters_from_filepath(filepath: str):
    k, qi_set = None, []
    base_filepath = os.path.basename(filepath)
    fp = base_filepath.split('.csv')[0]
    parts_1 = fp.split('_k=')
    try:
        k = int(parts_1[-1])
    except:
        pass
    parts_2 = parts_1[0].split('QI=')
    try:
        qi_set = parts_2[-1].split(',')
    except:
        pass
    return k, qi_set

def get_data_from_file(filepath):
    f = open(filepath, "r")
    lines = [line.strip("\n").split(",") for line in f]
    columns = lines[0]
    data = []
    for line in lines[1:]:
        d = {columns[i]: word for i, word in enumerate(line)}
        data.append(d)
    return data