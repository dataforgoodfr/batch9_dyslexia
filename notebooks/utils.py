import os
from os.path import join, isdir, isfile
from os import listdir


def load_all_files_path():
    # Get all directories with examples
    example_path = '../Exemples/'
    subdir_paths = [
        join(example_path, p) for p in listdir(example_path)
        if isdir(join(example_path, p))
    ]

    # Retrieves all files in example dir
    all_files = []
    for p in [example_path] + subdir_paths:
        _files = [join(p, f) for f in listdir(p) if isfile(join(p, f))]

        all_files = all_files + _files

    # Keeps only jpg extension files
    all_files = [f for f in all_files if f[-3:] in ['jpg']]

    return subdir_paths, all_files