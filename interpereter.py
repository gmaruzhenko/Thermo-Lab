import sys


"""
Initializes a file for writing and returns the file name
"""
def csv_init():

    print("Enter output file name (e.g. data.csv):")
    filename = input()


def csv_teardown(filename):
    filename.close()

