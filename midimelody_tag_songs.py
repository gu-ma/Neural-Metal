# Browse the midi melody folder and get tags from the musicbrainzngs API
# NEEDS TO BE FIXED so that it does not overwrite and eventually create new entries

import sys
import os
import sqlite3
from time import sleep
import musicbrainzngs as m

# static path to the midimelody files
MIDIMELODY_PATH = os.path.join(os.getcwd(), '..', 'midi', 'en.midimelody.ru')
MIDIMELODY_DB = os.path.join(MIDIMELODY_PATH, '_midimelody_ru.db')


def set_user_agent():

    m.set_useragent(
        "Midi Classification",
        "0.1",
        "http://massol.me"
    )


def get_artist_tags(artist, limit, strict=False):

    # not very accurate and causes problem if the limit is not set to 1 (we just get the first result)
    # but good enough for now for what we want to do
    tags_string = ''
    result = m.search_artists(limit=limit, artist=artist, strict=strict)
    for artist in result['artist-list']:
        # print(u"\n{id}: {name}".format(id=artist['id'], name=artist["name"]))
        print(u"|______\t{name} ({score}%)".format(score=artist['ext:score'], name=artist["name"]))
        tags = artist.get("tag-list", "")
        # add 000 in front of the counter
        for tag in tags:
            tag['count'] = '{:0>4}'.format(tag.get("count", ""))
        # sort by number of tags (ascending)
        import operator
        sorted_tags = sorted(
            tags, key=operator.itemgetter('count'), reverse=True)
        # print and add to returned string
        for tag in sorted_tags:
            name = tag.get("name", "")
            count = tag.get("count", "")
            print("|\t" + name + "(" + count + ")")
            tags_string += name + ', '
    return tags_string


# def updateFilePath():

#     conn = sqlite3.connect('_midimelody_ru.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM tracks")
#     # for row in c:
#     #     print(row)
#     index = 0
#     # Browse all folders and sub folders in the current directory
#     for root, subdirs, files in os.walk('.'):
#         for filename in files:
#             if filename.lower().endswith('.mid'):
#                 file_path = os.path.join(root, filename)
#                 index += 1
#                 c.execute("UPDATE tracks Set midi_files_path=?, WHERE Midi_Files=? AND artist=?", file_path, filename, );
#                 print(c.fetchone())


def walk_dir(start='', end=''):

    index = 0
    # Browse all folders and sub folders in the current directory
    for root, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            if index < end and index >= start:
                print(str(index) + ' | %s ' % subdir)
                index += 1


def main():

    conn = sqlite3.connect(MIDIMELODY_DB)
    c = conn.cursor()
    c.execute("SELECT DISTINCT artist FROM tracks")
    artists = [row[0] for row in c]
    #
    set_user_agent()
    #
    for artist in artists:
        print("\n" + artist)
        tags = get_artist_tags(artist, 1, False)
        # c.execute("UPDATE tracks Set tags=? WHERE artist=?", (tags, artist))
        # conn.commit()
        # sleep(1)
        pass


if __name__ == '__main__':
    sys.exit(main())
