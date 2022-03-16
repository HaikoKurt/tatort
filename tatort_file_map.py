#!/usr/bin/env python3
import os
from pathlib import Path
from renamer import Renamer

SOURCE_DIR = "/Users/haiko/Documents/Temp/Filme/Tatort"
DEST_DIR = "/Users/haiko/Documents/Temp/Tatort"
DUPLICATE_DIR = "/Users/haiko/Documents/Temp/Tatort-Doppelt"

def move(source, dest) :
    try :
        os.makedirs(os.path.dirname(dest))
    except :
        pass
    os.rename(source, dest)

# regular expression to identify a file that is named with episode numbers from the total ordering
# capture group 1: episode number (total order)
# capture group 2: file name (excluding the extension ".mp4")
# E.g., "0586 Dunkle Wege.mp4":
#   capture group 1: "0586"
#   capture grpup 2: "Dunkle Wege"
# Episide numbers from https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen
# Also, note that all episode numbers are ALWAYS 4 digits (with leading zeros if required). This last
# requirement can easily be relaxed with a slightly different regex 
renamer = Renamer()

for f in Path(SOURCE_DIR).iterdir():
    if f.is_file() :
        new_name = renamer.rename(f.name)
        if new_name is not None :
            source = f"{f.parent}/{f.name}"
            dest = f"{DEST_DIR}/{new_name}"
            duplicate = f"{DUPLICATE_DIR}/{f.name}"
            # os.rename() actually renames and moves the file. If the destination already exists, it will be replaced
            if not os.path.isfile(dest) :
                move(source, dest)
            else :
                print(f"*** {f.name} duplicate")
                move(source, duplicate)
            # print the partial file name to the console for confirmation
            print(f"{source} -> {dest}")
        else :
            print(f"*** {f.name} not found")
