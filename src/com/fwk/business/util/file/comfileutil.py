from os import listdir
from os.path import isfile, join

def allfile(filepath) :
    files = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    print(files)
    return files

allfile('.')


