import time, os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from renamer import Renamer
from pathlib import Path
import shutil, logging
from logging.config import dictConfig
import json

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

def on_modified(event):
    try :
        f = Path(event.src_path)
        source = f"{f.parent}/{f.name}"
        start_size = 0
        if f.is_file() :
            start_size = os.path.getsize(source)
        now = datetime.now()
        if not f.name.startswith(".") and f.is_file() and start_size > 0 :
            logger.info(f"{now} - {source}; size = {start_size}")
            time.sleep(10)
            size = os.path.getsize(source)
            logger.info(f"{now} - {source}; size = {size}")
            if not size > start_size :
                logger.info(f"{now} - {source}, not growing ")
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
    except Exception as e :
        logger.error(f"!!! Exception {e} occured")

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True 
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_modified = on_modified

    my_observer = Observer()
    my_observer.schedule(my_event_handler, SOURCE_DIR, recursive=False)

    logger.info("Start watching...")
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
