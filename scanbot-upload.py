#!./venv/bin/python3
import os
import sys
import time
import subprocess
import configparser

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

#print (items)
#print("-----------------")
#print (folderlist)

while True:
    for item in folderlist:
        #print(folderlist[item])
        for root, subFolders, files in os.walk(os.path.join(pathBase,pathUpload,folderlist[item]['folder'])):
            for file in files:
                if os.path.splitext(file)[1] == ".pdf":
                    uploadfile = os.path.join(pathBase,pathUpload,folderlist[item]['folder'],file)
                    print('foundone: ' + uploadfile)
                    print ("curl", "-u", folderlist[item]['userpwd'],"-T", uploadfile, folderlist[item]['upload'] + '/' + file)
                    try:
                        uploadprocess = subprocess.call(["curl", "-u", folderlist[item]['userpwd'],"-T", uploadfile, folderlist[item]['upload'] + '/' + file  ])
                        if uploadprocess == 0:
                            print("upload complete")
                            exitok = True
                        else:
                            print("CURL returned exit code: " + uploadprocess)
                            exitok = False
                    except Exception as e:
                        print("Unexpected error:", e)
                        exitok = False
                            
                    if exitok:
                        os.remove(uploadfile)
                        print("All ok. Removed file: " + uploadfile)
                    else:
                        os.rename(uploadfile, os.path.join(pathError,file))
                        print("Error... Moved file to error folder: " + uploadfile)          
    time.sleep(10)