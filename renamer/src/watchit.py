import os, json, shutil, logging
from logging.config import dictConfig
from renamer import Renamer
from watchfolder import Watchfolder

with open('logging.json', 'rt') as file :
    dictConfig(json.load(file))

SOURCE_DIR = "/source"
DEST_DIR = "/destination"
DUPLICATE_DIR = "/source/duplicate"
UNKNOWN_DIR = "/source/unknown"

renamer = Renamer()
logger = logging.getLogger(__name__)

def move(source, dest) :
    try :
        os.makedirs(os.path.dirname(dest))
    except :
        pass
    shutil.move(source, dest)
    logger.info(f"{source} -> {dest}")

def file_arrived(f):
    source = f"{f.parent}/{f.name}"
    new_name = renamer.rename(f.name)
    if new_name is not None :
        dest = f"{DEST_DIR}/{new_name}"
        duplicate = f"{DUPLICATE_DIR}/{f.name}"
        if not os.path.isfile(dest) :
            logger.info(f">>> {f.name} moved")
            move(source, dest)
        else :
            logger.info(f"*** {f.name} duplicate")
            move(source, duplicate)
    else :
        logger.info(f"??? {f.name} not found")
        unknown = f"{UNKNOWN_DIR}/{f.name}"
        move(source, unknown)

if __name__ == "__main__":
    logger.info("Start watching...")
    wf = Watchfolder(SOURCE_DIR, action = file_arrived)
    try :
        wf.watch()
    except KeyboardInterrupt :
        pass