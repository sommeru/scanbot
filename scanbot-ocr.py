import os
import sys
import subprocess

ocrdir = "out"

for root, subFolders, files in os.walk(ocrdir):
    if len (files) > 0:
        if os.path.splitext(files[0])[1] == ".pdf":
                print ("Found one: " + os.path.join(root,files[0]))
                ocrprocess = subprocess.run(["ocrmypdf", os.path.join(root,files[0]), "out.pdf", "--redo-ocr"], capture_output=True)
                print (ocrprocess.stdout)
                print (ocrprocess.returncode)

  