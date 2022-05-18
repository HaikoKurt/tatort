from pathlib import Path
from time import sleep
import _thread, os, logging

class Watchfolder :
    logger = logging.getLogger(__name__)

    def __init__(self, folder, action = None, no_system_files = True, watch_size_period = 10, watch_dir_period = 1) -> None:
        self.folder = folder
        self.no_system_files = no_system_files
        self.watch_size_period = watch_size_period
        self.watch_dir_period = watch_dir_period
        self.under_observation = []
        self.action = action

    def __wait_and_execute(self, f) :
        self.logger.info(f"waiting for {f.name}")
        source = f"{f.parent}/{f.name}"
        size = 0
        while size == 0 or size < os.path.getsize(source) :
            size = os.path.getsize(source)
            self.logger.debug(f"{f.name} size: {size}")
            sleep(self.watch_size_period)
        self.logger.debug(f"{f.name} ready...")
        try :
            if self.action is None :
                f.unlink(missing_ok=True)
            else :
                self.action(f)
        except Exception as e:
            self.logger.error(f"Exception occured: {e}")
        finally :
            self.under_observation.remove(f.name)

    def __test_and_start(self, f) :
        if f.is_file() and (not self.no_system_files or not f.name.startswith('.')) :
            if not f.name in self.under_observation :
                self.under_observation.append(f.name)
                _thread.start_new_thread(self.__wait_and_execute, (f, ))

    def watch(self) :
        while True :
            for f in Path(self.folder).iterdir():
                self.__test_and_start(f)
            sleep(self.watch_dir_period)

if __name__ == "__main__" :
    def move(f) :
        print(f"Moving: {f.name}")
        f.rename(f"/Users/haiko/Documents/Temp/destination/{f.name}")

    wf = Watchfolder("/Users/haiko/Documents/Temp/watchfolder", action = move)
    try :
        wf.watch()
    except KeyboardInterrupt :
        pass