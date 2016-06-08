import sys, re

def main(fname):
    sys.stdout.write(convert(fname) + '\n')

def convert(path):
    """
    Given a path to a .curlrc file, generates and returns
    a command-line curl statement.
    """
    full_cmd = 'curl '
    with open(path, 'r') as conf:
        for line in conf.readlines():
            if len(line.strip()) > 0:
                if line.strip()[0] != '#': # if not comment line
                    line = line.strip()
                    opt_val = map(lambda x: x.strip(), line.split(' = '))
                    if len(opt_val) > 1:
                        opt, val = opt_val
                        val = val.strip('\"')
                    else:
                        opt, val = opt_val[0], None
                    if opt[0] != '-': # if not shortcut, prefix --
                        opt = '--' + opt
                    # append to full command
                    full_cmd += '{} '.format(opt)
                    full_cmd += '{} '.format(val) if val else ''
    
    return full_cmd

if __name__ == '__main__':
    main(sys.argv[1])
