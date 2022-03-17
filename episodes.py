from encodings import utf_8
import http.client
import re

class Episodes :
    EPISODE_PATTERN = "(?s)\s*<td>(\d+)\s*<.*?title.*?>(.*?)[<&].*?"
    EPISODE_EXP = re.compile(EPISODE_PATTERN)
    TR_PATTERN = "(?si)<tr>(.*?)</tr>"
    TR_EXP = re.compile(TR_PATTERN)

    def __init__(self) -> None:
        conn = http.client.HTTPSConnection("de.wikipedia.org")
        conn.request("GET", "/wiki/Liste_der_Tatort-Folgen")
        response = conn.getresponse()
        self.episodes = dict(sorted(self.parse(response.read().decode("utf-8")).items(), key=lambda item: len(item[1]), reverse=True))
        conn.close()

    def parse(self, html) :
        result = {}
        for row in self.TR_EXP.findall(html) :
            match = self.EPISODE_EXP.fullmatch(row)
            if match is not None :
                result[int(match.group(1))] = match.group(2)
        return result

    def dump(self) :
        for episode in self.episodes :
            print(f"{episode} = {self.episodes[episode]}")

    NORMALIZE = [
        (b'u\xcc\x88'.decode("utf-8"), "ue"),
        ('ü', "ue"),
        (b'o\xcc\x88'.decode("utf-8"), "oe"),
        ('ö', "oe"),
        (b'a\xcc\x88'.decode("utf-8"), "ae"),
        ('ä', "ae"),
        ('!', ""),
        ('ß', "ss"),
        (b'A\xcc\x88'.decode("utf-8"), "Ae"),
        ('Ä', "Ae"),
        (b'U\xcc\x88'.decode("utf-8"), "Ue"),
        ('Ü', "Ue"),
        (b'O\xcc\x88'.decode("utf-8"), "Oe"),
        ('Ö', "Oe"),
        (" ", "_")
    ]

    def __normalize(self, string : str) :
        for replacement in self.NORMALIZE :
            string = string.replace(replacement[0], replacement[1])
        return string.upper()

    def file_title(self, episode) :
        to_strip = ['!', '?', '’', '–', '\'', ',']
        title = self.episodes[episode]
        for strip in to_strip :
            title = title.replace(strip, "")
        return title

    def find(self, filename: str) :
        norm_filename = self.__normalize(filename)
        for episode in self.episodes :
            norm_episode = self.__normalize(self.episodes[episode])
            if norm_filename.find(norm_episode) >= 0 :
                return episode
        return None

if __name__ == "__main__" :
    '''
    filenames = [
        "Tatort_Schimanski___restauriert_in_HD-Katjas_Schweigen_(1989)-2096889429.mp4",
        "Tatort-Alle_meine_Jungs-0248914024.mp4",
        "Tatort-Auf_ewig_Dein_(2014)-0369481507.txt",
        "0209_Einzelhaft_(1988)-2092373979.txt"
    ]
    e = Episodes()
    for filename in filenames :
        print(f"{filename} -> {e.find(filename)}")
    '''
    e = Episodes()
    e.dump()
