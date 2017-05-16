#!/usr/bin/env python
#####################################
# JpegLabel. 11th May 2017
#####################################

'''
Simple command line tool to rename jpegs by their EXIF date
(DateTimeOriginal)

usage: jpeglabel [directory]

Example:
    renames a file to '2016 12 04.jpg' (year month day)
'''

import sys
import os
import exifread

def parse_args():
    ''' Get the source directory from command line arguemnt'''
    args = sys.argv[1:]
    if not len(args) == 1:
        print("usage: jpeglabel [directory]")
        sys.exit(1)
    return args[0] 


def get_filenames(directory):
    '''
    Find all the jpg files in a directory

    Args:
        directory(str): The directory to search for files

    Returns:
        list of strings: The files, with absolute paths
    '''
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(directory)):
        break
    output = []
    for file in filenames:
        if '.jpg' in file.lower()[-4:]:
            output.append(dirpath + '/' + file)
    if not output:
        print("No files found")
        sys.exit(1)
    return output


def get_exif_data(file):
    '''
    Returns photo date in string format, or None if no exif data
    '''
    f = open(file, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image DateTime' in tags:
        dateTime = str(tags['EXIF DateTimeOriginal'])
        year = dateTime[0:4]
        month = dateTime[5:7]
        day = dateTime[8:10]
        return year + ' ' + month + ' ' + day
    else:
        return None

def rename_file(file, photo_date):
    '''Rename a jpg'''
    count = 1
    new_file_name = photo_date + '.jpg'
    while os.path.exists(new_file_name):
        # File already exists so try adding a number to make a new name
        new_file_name = photo_date + ' ' + str(count) + '.jpg'
        count += 1
    os.rename(file, new_file_name)
    return


def main():
    directory = parse_args()
    filenames = get_filenames(directory)
    for file in filenames:
        photo_date = get_exif_data(file)
        if photo_date:
            new_name = os.path.join(directory, photo_date)
            rename_file(file, new_name)


if __name__ == '__main__':
    main()
