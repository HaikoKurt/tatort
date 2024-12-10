import re
from episodes import Episodes

class Renamer :
    PATTERN = ".*?(\.[\d\w]{3})"
    REG_EXP = re.compile(PATTERN)

    # List of season tuples. The first entry in the tuple is the first episode number (based on total
    # ordering: https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen). Make sure this list is sorted
    # descending by episode number
    SEASONS = sorted([(1255, '2024'), (1220, '2023'), (1184, '2022'), (1151, '2021'), (1115, '2020'), (1078, '2019'),
                      (1041, '2018'), (1006, '2017'), (969, '2016'), (929, '2015'), (893, '2014'),
                      (857, '2013'), (822, '2012'), (786, '2011'), (751, '2010'), (717, '2009'),
                      (686, '2008'), (651, '2007'), (619, '2006'), (584, '2005'), (554, '2004'),
                      (521, '2003'), (490, '2002'), (461, '2001'), (432, '2000'), (403, '1999'),
                      (377, '1998'), (350, '1997'), (323, '1996'), (302, '1995'), (286, '1994'),
                      (268, '1993'), (253, '1992'), (238, '1991'), (227, '1990'), (215, '1989'),
                      (201, '1988'), (189, '1987'), (177, '1986'), (165, '1985'), (153, '1984'),
                      (144, '1983'), (132, '1982'), (120, '1981'), (108, '1980'), (95, '1979'),
                      (83, '1978'), (70, '1977'), (59, '1976'), (47, '1975'), (36, '1974'),
                      (25, '1973'),(14, '1972'), (3, '1971'), (1, '1970')],
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
            return f"{season[1]}/Tatort - (S{season[1]}_E{episode_no:02d}) - {self.episodes.file_title(absolute_episode_no)}{ext}"
        else :
            return None

if __name__ == "__main__" :
    names = [ 
        "Tatort-Borowski_und_die_Rückkehr_des_stillen_Gastes-0346044472.txt",
        "Tatort-Das_ewig_Böse-2090257250.txt",
        "Tatort-Tatort__Söhne_und_Väter-1549986488.txt",
        "Tatort-Amour_fou-1538445053.mp4",
        "Tatort-Für_immer_und_dich-0827701224.txt",
        "Tatort-Tatort__Der_irre_Iwan-1173230014.mp4",
        "Tatort-Tatort__Saarbrücken_an_einem_Montag-1211983919.mp4",
        "Tatort-Tatort__Chateau_Mort-0048477545.txt",
        "Tatort-Die_Blume_des_Bösen_(2007)-1873218538.txt",
        "Tatort-Mord_Ex_Machina-1016382991.txt",
        "Tatort_Schimanski___restauriert_in_HD-Freunde_(1986)-0668847862.txt",
        "Tatort-Tatort__Mia_san_jetz_da_wo's_weh_tut-1760368132.txt",
        "Tatort-Der_Tod_der_anderen_(2021)-0912978069.txt",
        "Tatort-Erntedank_e.V.-1671880365.mp4",     # wird nicht gefunden, da Titel aus Wikipedia nicht mit Mediathek übereinstimmt
        "Tatort-In_der_Familie_2-1394444053.txt",   # siehe oben
        "Ratort-Söhne_und_Väter-1549986488.txt",    # wird nicht gefunden, da der Dateiname nicht mit 'Tatort' beginnt
        ]
    renamer = Renamer()
    for old_name in names :
        new_name = renamer.rename(old_name)
        print(f"{old_name} -> {new_name}")
