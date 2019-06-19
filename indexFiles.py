# This script will index files in a specific directory and all sub directories
#   the index will consist of a dict containing the file details
#     name, md5sum, size, ...
# This dict will then be dumped to disk for reading by another script to do something with that information

import os
from MUFUtils import md5sumOfFile, save_obj, md5sum
import logging

logging.basicConfig(level=logging.DEBUG)


# path = "static\\images"
base_dir = os.getcwd()
path = r'.\static\images'


# main list of files with details
mainFilesIndex = dict()
# dict of md5sums to list of matching files
md5sumToFile = dict()

# r=root, d=directories, f = files
for root, directories, files in os.walk(path):
    logging.debug("| Working through root {}, dir {}, files {}".format(root, directories, files))
    for file in files:
        logging.debug("  | Cycling through files [{}], working on {}".format(files, file))
        thisMD5Sum = md5sumOfFile(os.path.join(root, file))
        logging.debug("    | {} has md5sum of {}".format(file, thisMD5Sum))
        relativePathToFile = os.path.join(root, file)
        logging.debug("    | {} has relative path of {}".format(file, relativePathToFile))
        MD5sumOfRelativePath = md5sum(relativePathToFile.encode('utf-8'))
        fullFileName = os.path.join(os.path.abspath(root), file)
        logging.debug("    | {} has full file name of {}".format(file, fullFileName))
        mainFilesIndex[MD5sumOfRelativePath] = {'fullFileName': fullFileName, 'fileName': file, 'md5sum': thisMD5Sum, 'relativePathToFile': relativePathToFile}
        logging.debug("    | {} added to mainFilesIndex with a key of {}".format(file, MD5sumOfRelativePath))
        logging.debug("    | mainFilesIndex for this key {} contains {}".format(MD5sumOfRelativePath, mainFilesIndex[MD5sumOfRelativePath]))
        for key, value in mainFilesIndex.items():
            logging.debug("      | mainFilesIndex: {}".format(key))
            # logging.debug("        | with values {}".format(value))
            for subKey, subValue in value.items():
                logging.debug("        | key [{}] = value [{}]".format(subKey, subValue))
        if thisMD5Sum in md5sumToFile:
            logging.debug("    | {} has md5sum of {} which has already been seen, adding reference {} to md5sumToFile".format(file, thisMD5Sum, MD5sumOfRelativePath))
            md5sumToFile[thisMD5Sum].append(MD5sumOfRelativePath)
        else:
            logging.debug("    | {} has md5sum of {}, this is the first time we've seen it".format(file, thisMD5Sum))
            md5sumToFile[thisMD5Sum] = [MD5sumOfRelativePath, ]

        logging.debug("    | next file ")
        logging.debug("")
        # logging.debug("Created a dict of dicts, the inner dict has the key " + relativePathToFile +
        #       " a sum of " + mainFilesIndex[relativePathToFile]['md5sum'])
        # logging.debug(mainFilesIndex[relativePathToFile])

logging.debug("Persisting Files...")
save_obj(mainFilesIndex, "mainFilesIndex")

logging.debug("Persisting sumToFile...")
save_obj(md5sumToFile, "md5sumToFile")

# ext = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv",
#        ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
#        ".rm", ".swf", ".vob", ".wmv" ".docx", ".pdf", ".rar",
#        ".jpg", ".jpeg", ".png", ".tiff", ".zip", ".7z", ".exe",
#        ".tar.gz", ".tar", ".mp3", ".sh", ".c", ".cpp", ".h",
#        ".gif", ".txt", ".py", ".pyc", ".jar", ".sql", ".bundle",
#        ".sqlite3", ".html", ".php", ".log", ".bak", ".deb"]
#
# files_to_enc = []
# for root, dirs, files in os.walk("/"):
#     for file in files:
#         if file.endswith(tuple(ext)):
#             files_to_enc.append(os.path.join(root, file))





