import argparse
import re
import os.path
import os
import shutil
import time
import sys
import io
import shutil

ALLOWED_FILES = ['srt']

def ParseInput():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file or directory")
    args = parser.parse_args()

    f = args.input
    print(f)
    if f:
        if (os.path.isfile(f)):
            return [f]
        elif (os.path.isdir(f)):
            fileList = GetFileList(f)
            return fileList
        elif (os.path.isdir(f[:-1])):
            fileList = GetFileList(f[:-1])
            return fileList
    return None

def GetFileList(dir):
    list = []
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, f)):
            if (re.split('[.]', f)[-1] in ALLOWED_FILES):
                list.append(os.path.join(dir, f))
    return list

def ReversePuctuation(file, newfile):
    f = io.open(file, 'r', encoding="utf8")
    nf = io.open(newfile, 'w', encoding="utf8")
    for line in f:
        if any("\u0590" <= c <= "\u05EA" for c in line):
            nf.write(FixOneLine(line))
        else:
            nf.write(line)
    f.close()
    nf.close()
    
def FixOneLine(s):
    directionalFormatting2b = '\u202b'

    # Amazon started adding "Pop Directional Formatting" - we are removing all of them from each line and replacing them.
    s = s.replace('\u202c', '')
    s = s.replace(directionalFormatting2b, '')
    
    return directionalFormatting2b + s 

def Main():
    provider0 = sys.argv[0]
    provider1 = sys.argv[1]
    provider2 = sys.argv[2]
    print("\narg0: " + provider0)
    print("\narg1: " + provider1)
    print("\narg2: " + provider2)
    if ".mkv_" not in provider2:
        print('Not from embeddedsubtitles provider. Terminating.')
        return

    fileList = ["".join(sys.argv[1])]
    if (not fileList):
        print('Usage: Select file')
        return

    print("Found " + str(len(fileList)) + " files. Starting to convert")
    
    for file in fileList:
        print("Converting File: " + re.split(r'[\\]', file)[-1])
        newFile = ".".join(re.split('[.]', file)[:-1]) + ".REV.he.srt"        
        ReversePuctuation(file, newFile)        
        os.remove(file)
        os.rename(newFile, file)

    print ('total files: ' + str(len(fileList)))
    
    time.sleep(1)


if __name__ == '__main__':
    Main()
