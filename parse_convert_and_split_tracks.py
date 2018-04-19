# parse the midi files in the input folder, convert them to abc
# split tracks and save

import os
import sys
import subprocess
import re

# string containing all midi files converted to abc notation
abc_raw_txt = ""


def extract_text(regex, txt):
    output = ""
    # extract
    for result in re.findall(regex, txt, re.S):
        output += result + "\n"
    # delete
    global abc_raw_txt
    abc_raw_txt = (re.sub(regex, '', abc_raw_txt, flags=re.S))
    # remove empty lines
    # abc_raw_txt = ''.join(line.lstrip(' \t') for line in abc_raw_txt.splitlines(True))
    abc_raw_txt = ''.join([s for s in abc_raw_txt.strip().splitlines(True) if s.strip()])
    return output


def delete_line(regex, txt):
    txt = (re.sub(regex, '', txt, flags=re.S))
    txt = ''.join([s for s in txt.strip().splitlines(True) if s.strip()])
    return txt


def main():
    # Variables
    script, input_folder_fp, output_folder_fp, set_name = sys.argv
    print('input_folder_fp = ' + input_folder_fp)
    print('output_folder_fp = ' + output_folder_fp)
    print('set_name = ' + set_name)
    # Output file containing all the abc text concatenated
    abc_file_fp = os.path.join(output_folder_fp, set_name + '.txt')
    global abc_raw_txt
    # instruments
    instruments_range = [
        range(-2, -1),
        range(-1, 0),
        range(0, 8),
        range(8, 16),
        range(16, 24),
        range(24, 32),
        range(32, 40),
        range(40, 56),
        range(56, 64),
        range(64, 72),
        range(72, 80),
        range(80, 104),
        range(104, 112),
        range(112, 120)
    ]
    # 
    instruments_name = [
        'headers',
        'drums',
        'piano',
        'percussion',
        'organ',
        'guitar',
        'bass',
        'strings',
        'brass',
        'reed',
        'pipe',
        'synth_lead',
        'ethnic',
        'percussive'
    ]
    # 
    instruments = {}
    for index, r in enumerate(instruments_range):
        for i in r:
            instruments[i] = instruments_name[index]
    print(instruments)
    # abc notation broken down by instruments
    abc_instruments_txt = {n: "" for n in instruments_name}
    # Convert all files in the input folders and save them in a txt variable
    for root, subdirs, files in os.walk(input_folder_fp):
        print('--\n' + root)
        for filename in files:
            file_path = os.path.join(root, filename)
            print('\t- %s ' % filename)
            if filename.lower().endswith('.mid'):
                p = subprocess.Popen(["midi2abc", file_path], stdout=subprocess.PIPE)
                (output, err) = p.communicate()
                abc_raw_txt += output.decode("utf-8")

    # Delete errors, comments and lyrics
    # http://abcnotation.com/wiki/abc:standard:v2.1#information_fields
    abc_raw_txt = delete_line(r'Error:.[^\n]*', abc_raw_txt)
    abc_raw_txt = delete_line(r'% .[^\n]*', abc_raw_txt)
    abc_raw_txt = delete_line(r'W; .[^\n]*', abc_raw_txt)

    # extract headers
    abc_instruments_txt['headers'] = extract_text(r'(X: 1.*?K:.[^\n]*)', abc_raw_txt)
    # print(abc_instruments_txt['headers'])

    # extract drums
    abc_instruments_txt['drums'] = extract_text(r'%%MIDI channel 10\n%%MIDI program 0\n(.*?)V:.[^\n]*', abc_raw_txt)
    # print(abc_instruments_txt['drums'])

    # extract instruments
    for result in re.findall(r'(%%MIDI program.[^\n]*.*?)V:.[^\n]*', abc_raw_txt, re.S):
        instrument_index = int(result.split()[2])
        if instrument_index in instruments:
            instrument_name = instruments[instrument_index]
            abc_instruments_txt[instrument_name] += result
            print(str(instrument_name))

    # write to files
    for key, value in list(abc_instruments_txt.items()):
        # 
        mypath = os.path.join(output_folder_fp, set_name)
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        # 
        abc_instrument_file_fp = os.path.join(output_folder_fp, set_name, key + '.txt')
        with open(abc_instrument_file_fp, 'w') as f:
            print("writing: " + str(abc_instrument_file_fp))
            value = delete_line(r'%%MIDI program.[^\n]*', value)
            f.write(value)


if __name__ == '__main__':
    sys.exit(main())

