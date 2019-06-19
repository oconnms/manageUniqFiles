from MUFUtils import load_obj, save_obj
from flask import Flask, render_template
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

mainFilesIndex = load_obj("mainFilesIndex")
md5sumToFile = load_obj("md5sumToFile")

@app.route('/')
def mainPage():
    # results = []
    #for md5sum, fileArray in md5sumToFile.iteritems():
        # print("Working on file: " + file['name'] + "(" + str(file['md5sum']) + ")<br>")
        # results.append({'name': file['name'], 'relatedFiles': md5sumToFile[file['md5sum']], 'md5sum': file['md5sum']})

        # print(str(type(f['md5sum'])))
        # for relatedFile in md5sumToFile[file['md5sum']]:
            # output = output + relatedFile + "\n<br>"

    logging.debug("pwd:" + os.getcwd())
    return render_template('main.html', md5sumToFile=md5sumToFile, mainFilesIndex=mainFilesIndex)

@app.route('/delete/<path:MD5sumOfRelativePath>', methods=['POST'])
def deleteFile(MD5sumOfRelativePath):
    logging.debug("| Deleting file ID {}".format(MD5sumOfRelativePath))
    try:
        fullFileName = mainFilesIndex[MD5sumOfRelativePath]['fullFileName']
        md5sumOfFileToRemove = mainFilesIndex[MD5sumOfRelativePath]['md5sum']
        logging.debug("| Which maps to {} with a sum of {}".format(fullFileName, md5sumOfFileToRemove))
    except KeyError:
        return render_template('main.html', md5sumToFile=md5sumToFile, mainFilesIndex=mainFilesIndex,
                               MD5sumOfRelativePath=MD5sumOfRelativePath,
                               error="rm: cannot remove '" + MD5sumOfRelativePath + "': No such file or directory")

    if os.path.exists(fullFileName):
        logging.debug("| Found {} on the filesystem".format(fullFileName))
        for key, value in mainFilesIndex[MD5sumOfRelativePath].items():
            logging.debug("  | key {} = value {}".format(key, value))
        if len(md5sumToFile[md5sumOfFileToRemove]) >= 2:
            os.remove(mainFilesIndex[MD5sumOfRelativePath]['fullFileName'])
            logging.debug("  | Deleting dict entry {} from mainFileIndex".format(MD5sumOfRelativePath))
            del mainFilesIndex[MD5sumOfRelativePath]
            logging.debug("  | Deleting array entry {} from md5sumToFile ".format(MD5sumOfRelativePath))
            md5sumToFile[md5sumOfFileToRemove].remove(MD5sumOfRelativePath)
        else:
            logging.debug("  | Can't delete this file, it's the last copy")

        logging.debug("  | There are {} elements left".format(len(md5sumToFile[md5sumOfFileToRemove])))

    else:
        return "[] doesn't exit, can't delete it".format()

    logging.debug("Persisting Files...")
    save_obj(mainFilesIndex, "mainFilesIndex")

    logging.debug("Persisting sumToFile...")
    save_obj(md5sumToFile, "md5sumToFile")

    logging.debug("pwd:" + os.getcwd())
    return render_template('main.html', md5sumToFile=md5sumToFile, mainFilesIndex=mainFilesIndex,
                           MD5sumOfRelativePath=MD5sumOfRelativePath, fullFileName=fullFileName)


app.run()
