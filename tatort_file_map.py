#!/usr/bin/env python3
import os
from pathlib import Path
import re

# List of season tuples. The first entry in the tuple is the first episode number (based on total
# ordering: https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen). Make sure this list is sorted
# descending by episode number
seasons = sorted([(1184, '2022'), (1151, '2021'), (1115, '2020'), (1078, '2019'), (1041, '2018'),
                  (1006, '2017'), (969, '2016'), (929, '2015'), (893, '2014'), (857, '2013'),
                  (822, '2012'), (786, '2011'), (751, '2010'), (717, '2009'), (686, '2008'),
                  (651, '2007'), (619, '2006'), (584, '2005'), (554, '2004'), (521, '2003'),
                  (490, '2002'), (461, '2001'), (432, '2000'), (403, '1999'), (377, '1998'),
                  (350, '1997'), (323, '1996'), (302, '1995'), (286, '1994'), (268, '1993'),
                  (253, '1992'), (238, '1991'), (227, '1990'), (215, '1989'), (201, '1988'),
                  (189, '1987'), (177, '1986'), (165, '1985'), (153, '1984'), (144, '1983'),
                  (132, '1982'), (120, '1981'), (108, '1980'), (95, '1979'), (83, '1978'),
                  (70, '1977'), (59, '1976'), (47, '1975'), (36, '1974'), (25, '1973'),(14, '1972'),
                  (3, '1971'), (1, '1970')],
                 key=lambda e: e[0], reverse=True)

# The NAS is mounted as "/mnt/All Media"
# Episodes are downloaded to the source_dir
source_dir = "/mnt/All Media/staging/"
# destination in the right format for Plex
dest_path = "/mnt/All Media/TV Shows (German)/Tatort {tvdb-83214}/Season "

# regular expression to identify a file that is named with episode numbers from the total ordering
# capture group 1: episode number (total order)
# capture group 2: file name (excluding the extension ".mp4")
# E.g., "0586 Dunkle Wege.mp4":
#   capture group 1: "0586"
#   capture grpup 2: "Dunkle Wege"
# Episide numbers from https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen
# Also, note that all episode numbers are ALWAYS 4 digits (with leading zeros if required). This last
# requirement can easily be relaxed with a slightly different regex 
exp = re.compile(r"(\d{4}) +(.+)\.mp4")

# iterate over all the files in the source directory
for f in Path(source_dir).iterdir():
    if f.is_file():
        fm = exp.fullmatch(f.name)
        # only rename/move the file if it matches the full regex
        if fm is not None:
            # capture group 1 is the episode number (e.g., 586)
            absolute_episode_no = int(fm.group(1))
            # determine season based on the season map above (e.g., the tuple (584, '2005'))
            season = next(t for t in seasons if t[0] <= absolute_episode_no)
            # calculate the relative episode number within the season (e.g., "03")
            episode_in_season = f"{absolute_episode_no - season[0] + 1:02d}"
            # capture group 2 is the file name (e.g., "Dunkle Wege")
            title = fm.group(2)
            # complete new file name. (e.g., "Tatort - s2005e03 - Dunkle Wege.mp4")
            dest_file = f"Tatort - s{season[1]}e{episode_in_season} - {title}.mp4"
            # determine complete source and destination path
            source = f"{f.parent}/{f.name}"
            dest = f"{dest_path}{season[1]}/{dest_file}"
            # os.rename() actually renames and moves the file. If the destination already exists, it will be replaced
            os.rename(source, dest)
            # print the partial file name to the console for confirmation
            print(f"s{season[1]}e{episode_in_season} - {title}")
