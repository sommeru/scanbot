#!./venv/bin/python3

import os
import sys
import time
import subprocess
import configparser

exitok = False

config = configparser.ConfigParser()
config.read('scanbot.conf')

folderlist = {}
for section in config.sections():
    if section.startswith('server'):
        folderlist[section] = {}
        for option in config.options(section):
            folderlist[section][option] = config.get(section, option)

pathBase = config['Path']['pathBase']
pathUpload = config['Path']['pathUpload']
pathError = config['Path']['pathError']
pathOCR = config['Path']['pathOCR']

def createDirs():
    for section in config.sections():
      if section.startswith('server'):
          createpath = os.path.join(pathUpload , folderlist[section]['folder'])
          if not os.path.exists(createpath):
              os.makedirs(createpath)
    if not os.path.exists(pathError):
            os.makedirs(pathError)

createDirs()     

while True:
    for root, subFolders, files in os.walk(pathOCR):
        for file in files:
            if os.path.splitext(file)[1] == ".pdf":
                    if __name__ == '__main__':
                        print('foundone: ' + os.path.join(root,file))
                        try:
                            outfile = os.path.join(root.replace(dirOCR, pathUpload),file)
                            infile = os.path.join(root,file)
                            ocrprocess = subprocess.call(["ocrmypdf", infile, outfile, "-l=deu+eng", "--deskew" ])
                        
                            if ocrprocess == 0:
                                print("OCR complete")
                                exitok = True
                            elif ocrprocess == 2:
                                print("Invalid PDF")
                                exitok = False
                            elif ocrprocess == 3:
                                print("Tesseract probably missing")
                                exitok = False
                            elif ocrprocess == 6:
                                print("OCR already done")
                                exitok = False
                            else:
                                exitok = False

                        except Exception as e:
                            print("Unexpected error:", e)
                            exitok = False
                        
                        if exitok:
                            os.remove(infile)
                            print("All ok. Removed file: " + infile)
                        else:
                            os.rename(infile, os.path.join(pathError,file))
                            print("Error... Moved file to error folder: " + infile)                  
    time.sleep(10)




  