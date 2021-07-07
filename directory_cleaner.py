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
import datetime
import calendar

CURRENT_YEAR = int(str(datetime.date.today())[:4])
MINIMUM_YEAR = 1950

# TODO: remove dir not working because of .DS_Store file
# TODO: fix file exists error in organize_clutter
# TODO: make this module a class called DirectoryCleaner
# TODO: "custom" option in get_dirty_files only works with groups
# TODO: get_dirty_files could only pre-sort by name, what about file date or size?

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

def get_dirty_files(path: str, by="filetype") -> dict :
    file_type = defaultdict(list)
    if by == "nameyear":
        regexpression = "([\d][\d][\d][\d])"
    elif by == "namemonth":
        regexpression = "-([\d][\d])-"
    elif by == "custom":
        regexpression = input("\nPlease enter a custom regex expression: ")
    else:
        regexpression = "([\w]+)$" # default regex is by filetype (e.g. png, jpg)

    try:
        for item in os.scandir(path):
            if item.is_file():
                match = re.search(regexpression, item.name)
                if match:
                    if by == "nameyear": # sort subdirectories by year in file name
                        print(match.group(1))
                        if int(match.group(1)) < MINIMUM_YEAR or int(match.group(1)) > CURRENT_YEAR:
                            print("No match:", item.name)
                            file_type["Other"].append(item.name)
                        else:
                            file_type[match.group(1)].append(item.name)

                    elif by == "namemonth": # sort subdirectories by month in file name
                        file_type[calendar.month_name[int(match.group(1))]].append(item.name)

                    else:
                        file_type[match.group(1)].append(item.name)
                else:
                    print("No match:", item.name)
                    file_type["Other"].append(item.name)
    except FileNotFoundError as error:
        print(str(error))
    return file_type # returns a dictionary with keys as subdirectory names and values as lists of file names

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

def organize_clutter(dirty_files: dict, path: str, drop=False):
    try:
        for file_type in dirty_files.keys():
            os.makedirs(path + os.sep + file_type)
        for file_type, files in dirty_files.items():
            for file in files:
                if drop:
                    shutil.move(path + os.sep + file, path + os.sep + file_type)
                else:
                    shutil.copy(path + os.sep + file, path + os.sep + file_type)
    except FileExistsError:
        print("There is a directory with a name that already exists.")

if __name__ == "__main__":
    path = get_dirty_dir()
    files = get_dirty_files(path, by="custom")
    remove_empty_dir(path)
    organize_clutter(files, path)
