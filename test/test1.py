import sys
import time
import msvcrt


def timeout_input(caption, default, timeout=5):
    start_time = time.time()
    # sys.stdout.write('%s(%s):' % (caption, default))
    sys.stdout.write(caption)
    sys.stdout.flush()
    _input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13:         # enter_key
                break
            elif ord(byte_arr) >= 32:       # space_char
                _input += "".join(map(chr, byte_arr))
        if len(_input) == 0 and (time.time() - start_time) > timeout:
            print(default, end='')
            break
        else:
            remain_time = '%02d' % (timeout - int(time.time() - start_time) -1)
            print('\r'+f"[{remain_time}]"+'%s:' % caption, end="")
    print('')  # needed to move to next line
    if len(_input) > 0:
        return _input
    else:
        return default


if __name__ == '__main__':
    # and some examples of usage
    while True:
        ans = timeout_input('发动技能[y/n]', 'n')
