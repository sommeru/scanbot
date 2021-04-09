import os
import sys
import ocrmypdf
import logging
import time
import subprocess

dirOCR = "outRename"
dirOut = "outOCR"
dirError = "outError"
exitok = False

dirOutFolders =["general","ssms/doc","ssms/invoice","ifs/doc","ifs/invoice"]

def createDirs():
    for path in dirOutFolders:
        createpath = os.path.join(dirOut,path)
        if not os.path.exists(createpath):
            os.makedirs(createpath)
    if not os.path.exists(dirError):
            os.makedirs(dirError)

createDirs()     

while True:
    for root, subFolders, files in os.walk(dirOCR):
        for file in files:
            if os.path.splitext(file)[1] == ".pdf":
                    if __name__ == '__main__':
                        print('foundone: ' + os.path.join(root,file))
                        try:
                            outfile = os.path.join(root.replace(dirOCR, dirOut),file)
                            infile = os.path.join(root,file)
                            #result = ocrmypdf.ocr(infile,outfile, l="deu+eng", deskew=True)
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
                            os.rename(infile, os.path.join(dirError,file))
                            print("Error... Moved file to error folder: " + infile)                  
    time.sleep(10)




  