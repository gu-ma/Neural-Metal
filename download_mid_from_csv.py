# Download files from a CSV scrapping

import os
import sys
import csv
import urllib.request
import urllib.parse
import urllib.error
import plistlib
import xattr
import re
from time import sleep


def parse_csv(file_name):
    tracks_list = open(file_name, "r")
    return csv.reader(tracks_list)


def write_xattr_tags(file_path, tags):
    bpl_tags = plistlib.writePlistToString(tags)
    optional_tag = "com.apple.metadata:"
    map(lambda a: xattr.setxattr(file_path, optional_tag + a, bpl_tags),
        ["kMDItemFinderComment", "_kMDItemUserTags", "kMDItemOMUserTags"])


def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def save_midi_files(output_folder_fp, csv_fp, start='', end='', sleep_duration=.2):
    csv_reader = parse_csv(csv_fp)
    header = next(csv_reader)
    print(header)

    # change headers here depending on the CSV format
    # template for "midimelody_ru.csv"
    if "midimelody_ru.csv" in csv_fp:
        alphabet_index = header.index("alphabet")
        artist_index = header.index("artist")
        track_index = header.index("midi_files")
        url_index = header.index("midi_files_href")
    # template for "ninsheet.csv"
    elif "ninsheet.csv" in csv_fp:
        serie_index = header.index("series")
        title_index = header.index("title")
        url_index = header.index("mid-href")

    for index, row in enumerate(csv_reader):
        if index < end and index > start:

            # template for "midimelody_ru.csv"
            if "midimelody_ru.csv" in csv_fp:
                alphabet = row[alphabet_index]
                artist = row[artist_index]
                track = row[track_index]
                url = row[url_index]
                artist_path = os.path.join(output_folder_fp, alphabet, artist)
                song_path = os.path.join(artist_path, track)
                label = "x"
                if not os.path.isfile(song_path) and url:
                    create_path(artist_path)
                    urllib.request.urlretrieve(url, song_path)
                    label = "+"
                print(label + "  " + str(index) + "\t" + alphabet +
                      "\t" + artist + "\t" + track)

            # template for "ninsheet.csv"
            elif "ninsheet.csv" in csv_fp:
                serie = row[serie_index]
                title = row[title_index]
                url = row[url_index]
                artist_path = os.path.join(
                    output_folder_fp, re.sub('[^A-Za-z0-9]+', ' ', serie))
                song_path = os.path.join(artist_path, re.sub(
                    '[^A-Za-z0-9]+', ' ', title) + ".mid")
                label = "x"                
                if not os.path.isfile(song_path) and url:
                    create_path(artist_path)
                    urllib.request.urlretrieve(url, song_path)
                    label = "+"
                print(label + "  " + str(index) + "\t" + serie + "\t" + title)

            # TBD
            # 
            # tag_list1 = ['Rap', 'Yo']
            # write_xattr_tags(song_path, tag_list1)
            # plistlib.writePlist(tag_list1, song_path)
            #
            # with open(song_path, 'rb') as fp:
            #     pl = plistlib.readPlist(fp)
            # print(pl)
            # pl.append('Blue')
            # plistlib.writePlist(pl, song_path)

            sleep(sleep_duration)


def main():
    script, csv_fp, output_folder_fp = sys.argv
    save_midi_files(output_folder_fp, csv_fp, 0, 4000, .1)


if __name__ == '__main__':
    sys.exit(main())
