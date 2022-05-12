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

def TLB_lookup(TLB, page_num):
    for pnum, fnum in TLB:
        if pnum == page_num:
            return fnum
    return None


def get_next_frame(page_table, page_num, algo):
    frame_num = 0
    #implement algo
    return frame_num

def page_table_lookup(page_table, TLB, page_num, algo):
    #check if page_num in pt and valid
    #if not, fetch next frame num and update page table and increment page faults
    frame_num = get_next_frame(page_table, page_num, algo)
        #update page table
    #update TLB
    return page_table, TLB, frame_num


if __name__ == '__main__':
    file, num_frames, algo = read_args()
    print("simulating %d frames from %s with %s" % (num_frames, file, algo))
    addrs = read_file(file)
    #for i, addr in enumerate(addrs):
    #    print("%d: %s" % (i, addr))
    TLB = []
    page_table = []
    for addr in addrs:
        page_num = (int(addr) & 0xFF00) >> 8
        offset = int(addr) & 0xFF
        fnum = TLB_lookup(TLB, page_num)
        if fnum is None:
            #tlbmiss increment
            page_table, TLB, fnum = page_table_lookup(page_table, TLB, page_num, algo)
        #get target byte + frame
        #print info
    #print hit and fault rates