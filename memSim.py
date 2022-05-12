import sys


def read_file(filename):
    addrs = []
    try:
        file = open(filename, "r")
        for line in file:
            if not line.strip().isnumeric():
                print("\'%s\' formatted improperly in input file" % line)
                raise IOError
            addrs.append(line.strip())
    except:
        print("File not found or formatted incorrectly")
        exit(1)
    return addrs

def read_args():
    frames = 256
    algo = "FIFO"
    inputfile = None
    for i, arg in enumerate(sys.argv[1:]):
        if i == 0:
            inputfile = arg
        elif arg in ["FIFO", "LRU", "OPT"]:
            algo = arg
        elif arg.isnumeric():
            frames = int(arg)
            if frames > 256 or frames < 1:
                print("%d is an invalid number of frames. Use (0, 256]" % frames)
                exit(1)
    return inputfile, frames, algo


if __name__ == '__main__':
    file, num_frames, algo = read_args()
    print("simulating %d frames from %s with %s" % (num_frames, file, algo))
    addrs = read_file(file)
    for i, addr in enumerate(addrs):
        print("%d: %s" % (i, addr))
