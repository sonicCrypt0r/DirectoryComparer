#Written by Thomas Ascenzi

import os
from fnmatch import fnmatch
import hashlib


def main():
    pathA = "/"
    pathB = "/"
    
    listA = genList(pathA)
    listB = genList(pathB)

    i = 0
    while i < len(listA):
        print(str(i) + ": " + listA[i]["file"], listA[i]["checksum"])
        i = i + 1

    i = 0
    while i < len(listB):
        print(str(i) + ": " + listB[i]["file"], listB[i]["checksum"])
        i = i + 1

    listAnoPath = removePathFromList(listA, pathA)
    listBnoPath = removePathFromList(listB, pathB)

    i = 0
    while i < len(listB):
        if listBnoPath[i] not in listAnoPath:
            print("Missing File " + str(i) + ": " + listB[i]["file"], "[" + listB[i]["checksum"] + "]")
        i = i + 1

    return


def genList(root):
    listA = []

    for path, subdirs, files in os.walk(root):
        files = sorted(files)
        for name in files:
            filePath = os.path.join(path, name)
            listA = calcNameAndHash(filePath, listA)
        
    listA = sortByPath(listA)

    return listA


def calcNameAndHash(filePath, listA):
    print(filePath)
    if os.path.isfile(filePath):
        with open(filePath, "rb") as f:
            file_hash = hashlib.md5()
            y = 0
            while chunk := f.read(8192):
                file_hash.update(chunk)
                print(filePath + " Chunk " + str(y) + " [" + file_hash.hexdigest() + "]")
                y = y + 1
            checksum = file_hash.hexdigest()
            listA.append({"file": filePath, "checksum": checksum})
            print(filePath + " [" + checksum + "]")
    else:
        listA.append({"file": filePath, "checksum": ""})

    return listA


def sortByPath(listA):
    listA = sorted(listA, key = lambda i: str.lower(i['file']))
    return listA


def removePathFromList(listVar, path):
    i = 0
    while i < len(listVar):
        listVar[i]["file"] = listVar[i]["file"].replace(path, "")
        i = i + 1
 
    return listVar

main()