import re
from episodes import Episodes

class Renamer :
    PATTERN = ".*?(\.[\d\w]{3})"
    REG_EXP = re.compile(PATTERN)

    # List of season tuples. The first entry in the tuple is the first episode number (based on total
    # ordering: https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen). Make sure this list is sorted
    # descending by episode number
    SEASONS = sorted([(1184, '2022'), (1151, '2021'), (1115, '2020'), (1078, '2019'), (1041, '2018'),
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

    def __init__(self) -> None:
        self.episodes = Episodes()

    def rename(self, old_name) :
        fm = self.REG_EXP.fullmatch(old_name)
        absolute_episode_no = self.episodes.find(old_name)
        if fm is not None and absolute_episode_no is not None:
            ext = fm.group(1)
            season = next(t for t in self.SEASONS if t[0] <= absolute_episode_no)
            episode_no = absolute_episode_no - season[0] + 1
            return f"{season[1]}/Tatort - (S{season[1]}_E{episode_no:02d}) - {self.episodes.episodes[absolute_episode_no]}{ext}"
        else :
            return None

if __name__ == "__main__" :
    names = [ 
        "180_Der_Tausch_(1986)-1048101661.mp4",
        "0808_Altes_Eisen-1005771900.txt",
        "897-Adams_Alptraum___tatort-0369648692.mp4",
        "",
        "Tatort_Schimanski___restauriert_in_HD-Medizinmänner_(1990)-0410832502.txt"
        ]
    renamer = Renamer()
    for old_name in names :
        new_name = renamer.rename(old_name)
        print(f"{old_name} -> {new_name}")
