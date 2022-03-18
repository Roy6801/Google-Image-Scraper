from tkinter.filedialog import askdirectory
from urllib import request
from tkinter import Tk
import os


def checkDir(dName, cnt):
    if os.path.isdir(dName):
        dName = dName.replace(f" ({cnt - 1})", "")
        dName = dName + f" ({cnt})"
        return checkDir(dName, cnt + 1)
    else:
        return dName


def createDir(query, defaultDir, dirPath):
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    if dirPath is not None and len(dirPath) != 0:
        directory = dirPath + "\\GIS Downloads\\" + query
    else:
        if not defaultDir:
            directory = askdirectory(parent=root)
            if directory is not None and len(directory) != 0:
                directory = directory + "\\GIS Downloads\\" + query
                directory.replace("/", "\\")
            else:
                print("No Directory Selected... Creating Default Directory!")
                directory = os.getcwd() + "\\GIS Downloads\\" + query
        else:
            directory = os.getcwd() + "\\GIS Downloads\\" + query

    directory = checkDir(dName=directory, cnt=0)
    os.makedirs(directory, exist_ok=True)
    print("Saving to... ", directory)
    return directory


def download_images(query, images, dir, tCount=1, tid=0):
    totalTaskLength = len(images)
    taskLength = totalTaskLength // tCount
    chunkStart = tid * taskLength
    if tid == tCount - 1:
        chunkEnd = len(images)
    else:
        chunkEnd = chunkStart + taskLength

    opener = request.build_opener()
    opener.addheaders = [(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    )]
    request.install_opener(opener)
    for index in range(chunkStart, chunkEnd):
        img = images[index]
        file = f"{dir}\\{query}_{str(tid)}_{str(index).rjust(3,'0')}.jpg"
        try:
            request.urlretrieve(img, file)
        except Exception as e:
            pass


def saveToList(images, dirName, query):
    dirName = dirName + f"\\{query}.txt"
    with open(dirName, "a") as fa:
        for index, link in images.items():
            fa.write(f"{str(index)} : {link}\n")
