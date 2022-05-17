import sys
frame_queue = []
addr_index = 0

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


def FIFO():
    frame_num = frame_queue.pop(0)
    frame_queue.append(frame_num)
    return frame_num

def LRU(): #!implement me!
    frame_num = 0
    return frame_num

def OPT(): #!implement me!
    frame_num = 0
    return frame_num


def get_next_frame(page_num, algo, frame_table, addrs):
    frame_num = 0
    if algo == "FIFO":
        frame_num = FIFO()
    if algo == "LRU":
        frame_num = LRU()
    if algo == "OPT":
        frame_num = OPT()
    return frame_num

def updateTLB(TLB, page_num, frame_num):
    if len(TLB) > 15:
        TLB.remove(0)
    TLB.append((page_num, frame_num))
    return TLB

def page_table_lookup(page_table, page_num):
    #check if page_num in pt is valid
    if page_table[page_num][1]:
        updateTLB(TLB, page_num, page_table[page_num][0])
        return page_table[page_num][0]
    return None


def table_update(page_table, TLB, algo, frame_table, page_num, addrs):
    #if not, fetch next frame num and update page table
    frame_num = get_next_frame(page_num, algo, frame_table, addrs)
    page_table[page_num] = (frame_num, True)
    updateTLB(TLB, page_num, frame_num)
    return page_table, TLB, frame_num

if __name__ == '__main__':
    file, num_frames, algo = read_args()
    print("simulating %d frames from %s with %s" % (num_frames, file, algo))
    addrs = read_file(file)
    #for i, addr in enumerate(addrs):
    #    print("%d: %s" % (i, addr))
    TLB = []
    page_table = [(None, False)] * 256
    frame_table = [-1] * num_frames
    for num in range(num_frames):
        frame_queue.append(num)
    tlbmiss, page_faults = 0, 0
    for addr in addrs:
        page_num = (int(addr) & 0xFF00) >> 8
        #print(page_num)
        offset = int(addr) & 0xFF
        fnum = TLB_lookup(TLB, page_num)
        if fnum is None:
            tlbmiss += 1
            fnum = page_table_lookup(page_table, page_num)
            if fnum is None:
                page_faults += 1
                page_table, TLB, fnum = table_update(page_table, TLB, algo, frame_table, page_num, addrs)

        #get target byte + frame
        #print info
        addr_index += 1
    #print hit and fault rates