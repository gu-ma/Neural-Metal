# This script select and copy files automatically from the Midimelody folder
# to the 00-Process folder for them to be parsed later.

import sys
import os
import sqlite3
import shutil

# static path to the midimelody files
MIDIMELODY_PATH = os.path.join(os.getcwd(), '#midi', 'en.midimelody.ru')
MIDIMELODY_DB = os.path.join(MIDIMELODY_PATH, '_midimelody_ru.db')


def show_title():
     print(' _   _                      _   __  __      _        _ ')
     print('| \ | | ___ _   _ _ __ __ _| | |  \/  | ___| |_ __ _| |')
     print('|  \| |/ _ \ | | | \'__/ _` | | | |\/| |/ _ \ __/ _` | |')
     print('| |\  |  __/ |_| | | | (_| | | | |  | |  __/ || (_| | |')
     print('|_| \_|\___|\__,_|_|  \__,_|_| |_|  |_|\___|\__\__,_|_|')
     print('                                                       ')
     print('-------------------------------------------------------')

def delete_dir_content(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def choose_tag():
    conn = sqlite3.connect(MIDIMELODY_DB)
    c = conn.cursor()
    confirm = ''
    while confirm not in ('Y', 'y'):
        tag = input("\nSearch tag: "),
        c.execute("SELECT count(DISTINCT midi_files) FROM tracks WHERE INSTR(tags, ?)>0", tag)
        files_count = c.fetchone()[0]
        c.execute("SELECT count(DISTINCT artist) FROM tracks WHERE INSTR(tags, ?)>0", tag)
        artist_count = c.fetchone()[0]
        print("{:,}".format(files_count) + " files  |  " + "{:,}".format(artist_count) + " Artists\n--------")
        confirm = input("Use that tag? [y/n] ")
    return tag


def get_artists_list(tag):
    conn = sqlite3.connect(MIDIMELODY_DB)
    c = conn.cursor()
    c.execute("SELECT DISTINCT artist FROM tracks WHERE INSTR(tags, ?)>0", tag)
    return [row[0] for row in c]


def copy_files(artists, output_folder_fp):
    index = 0
    # Browse all folders and sub folders in the midimelody directory
    for root, subdirs, files in os.walk(MIDIMELODY_PATH):
        for subdir in subdirs:
            for artist in artists:
                if subdir == str(artist):
                    subdir_fp = os.path.join(root, subdir)
                    subdir_output_fp = os.path.join(output_folder_fp, subdir)
                    shutil.copytree(subdir_fp, subdir_output_fp)
                    print(str(index) + ' | %s ' % subdir_fp)
                    index += 1


def main():
    show_title();
    script, output_folder_fp = sys.argv
    # print(MIDIMELODY_PATH)
    tag = choose_tag()
    artists = get_artists_list(tag)
    # change after this
    delete_dir_content(output_folder_fp)
    copy_files(artists, output_folder_fp)


if __name__ == '__main__':
    sys.exit(main())
