'''
Author: Paolo Pedrigal
GitHub Account: paolopedrigal
Description: This program will be able to...
(1) Ask user for which directory to clean
(2) Organize cluttered files into folders, sorted by file type.
(3) Delete directories that contain empty files
'''

import os
import re
from collections import defaultdict
import shutil

# TODO: organize clutter
# TODO: make get_dirty_files_by_type more general, perhaps pass regex expression argument 

def get_dirty_dir() -> str :
    while True:
        try:      
            path = input("Path of directory to clean (or [Enter] to exit): ")
            if len(path) == 0:
                print("Exiting...")
                break    
            elif os.path.isdir(path):
                break   
        except FileNotFoundError as error:
            print(str(error))
    return path

def get_dirty_files_by_type(path: str) -> dict :
    file_type = defaultdict(list)
    try:
        for item in os.scandir(path):
            if item.is_file():
                match = re.search("([\w]+)$", item.name)
                if match:
                    file_type[match.group()].append(item.name)
                else:
                    print("No match:", item.name)
    except FileNotFoundError as error:
        print(str(error))
    return file_type

def remove_empty_dir(path: str) -> list :
    removed_dir = []
    try:
        for item in os.scandir(path):            
            if item.is_dir():
                if len(os.listdir(item.path)) == 0:
                    removed_dir.append(item.name)
                    os.rmdir(item.path)
    except FileNotFoundError as error:
        print(str(error))
    return removed_dir

def sort_by_date():
    # match = re.search("([\d]+\.[\d]+\.[\d]+)", item.name)
    # if match is not None:
    #     print(item.name, match.group())
    pass

def organize_clutter(file_types: dict, dest_path: str, drop=False):
    for file_type, files in file_types.items():
        for file in files:
            os.makedirs(dest_path + os.sep + file_type + os.sep + file)
        if drop:
            pass

if __name__ == "__main__":
    path = get_dirty_dir()
    files = get_dirty_files_by_type(path)
    organize_clutter(files, path)
