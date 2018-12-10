import os
import sys
import subprocess
import io
import time


TORCHRNN_PATH = os.path.join(os.getcwd(), '..', 'torch-rnn')
abc_path = os.path.join(os.getcwd(), '..', 'output', 'abc')
midi_path = os.path.join(os.getcwd(), '..', 'output', 'midi')


def main():
    script, checkpoint, length, temp, start_text, loops, key, instrument = sys.argv
    print('checkpoint = ' + checkpoint)
    print('length = ' + length)
    print('temp = ' + temp)
    print('start_text = ' + start_text)
    print('loops = ' + loops)
    print('key = ' + key)
    print('instrument = ' + instrument)
    # 
    sp1 = checkpoint.rsplit('.', 1)
    sp2 = sp1[0].split('/')
    checkpoint_name = sp2[len(sp2)-1]
    # sp3 = checkpoint_name.rsplit('_', 2)
    # checkpoint_name_shorten = sp3[len(sp3)-2]+"_"+sp3[len(sp3)-1]
    # 
    os.chdir(TORCHRNN_PATH)


    for i in range(int(loops)):

        # t = time.strftime('%Y%m%d%H%M%S')
        t = time.strftime('%M%S')
        counter = ('%02d' % i)
        file_name = instrument + "_K|" + key + "_" + counter + "_" + t + "_" + checkpoint_name

        print ("Creating " + os.path.join(abc_path, file_name + '.abc'))

        if os.path.isfile(os.path.join(abc_path, file_name + '.abc')):
            os.remove(os.path.join(abc_path, file_name + '.abc'))

        with open(os.path.join(abc_path, file_name + '.abc'), 'a') as abc_file:

            sample_cmd_list = [
                'th',
                'sample.lua',
                '-checkpoint',
                checkpoint,
                '-length',
                length,
                '-gpu',
                '-1',
                '-temperature',
                temp,
                '-start_text',
                start_text
            ]
            sample_proc = subprocess.Popen(
                sample_cmd_list,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )
            # (output, err) = sample_proc.communicate()
            output = sample_proc.stdout.read()
            midi_label = ''
            if instrument == 'drums':
                midi_label = '%%MIDI channel 10\n' 
            # abc_file.write( 'X:1\nT:'+checkpoint_name+"_"+str(float(temp))+"_"+str(i)+'\nM:4/4\nL:1/8\nQ:1/4=110\nK:' + key + '\nV:1\n%%MIDI channel 10\n'+ output)
            abc_file.write( 'X:1\nT:'+checkpoint_name+"_"+str(float(temp))+"_"+str(i)+'\nM:4/4\nL:1/8\nQ:1/4=110\nK:' + key + '\nV:1\n' + midi_label + output)

        time.sleep(1)
        convert_proc = subprocess.Popen(['abc2midi',os.path.join(abc_path, file_name + '.abc'),'-o',os.path.join(midi_path, file_name + '.mid')])
        convert_proc.communicate()


if __name__ == '__main__':
    sys.exit(main())
