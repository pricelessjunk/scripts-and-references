import os
import re

def walkme(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            if name[-4:] == '.mkv' and '300mbfilms' in name:

                newName = name[0:name.index(".")] + '.mkv'
                print(name + " -> " + newName)
                os.rename(os.path.join(root,name), os.path.join(root,newName))

        for name in dirs:
            walkme(name)


walkme(".")
