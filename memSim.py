import sys
frame_queue = []
addr_index = 0
recency_value = 0
def read_file(filename):
    addrs = []
    try:
        file = open(filename, "r")
        for line in file:
            if not line.strip().isnumeric():
                print("\'%s\' formatted improperly in input file" % line)
                raise IOError
            addrs.append(line.strip())
        file.close()
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

def get_minvalue(inputlist):
    # get the minimum value in the list
    min_value = min(inputlist)

    # return the index of minimum value
    min_index = inputlist.index(min_value)
    return min_index

def LRU(frame_table): #!implement me!
    frame_num = -1
    global recency_value
    #print(LRU_table)
    for i, entry in enumerate(frame_table):  # check if empty
        if entry == -1:
            frame_num = i
            LRU_table[i] = recency_value
            recency_value = recency_value + 1
            break;
    if frame_num == -1:  # if full, go to algorithm
        frame_num = get_minvalue(LRU_table) #get the minimum (last used index)
        LRU_table[frame_num] = recency_value #update the LRU table with the new recency value
        recency_value = recency_value + 1 #increment the recency value
    return frame_num

def OPT(frame_table, addrs): #!implement me!
    frame_num = -1
    for i, entry in enumerate(frame_table): #check if empty
        if entry == -1:
            frame_num = i
            break;
    if frame_num == -1: #if full, go to algorithm
        pnums = []
        for addr in addrs[addr_index + 1:]:
            pnums.append((int(addr) & 0xFF00) >> 8)
        fnexts = []
        for j, entry in enumerate(frame_table):
            next = -1
            for i, pnum in enumerate(pnums):
                if entry == pnum:
                    next = i
                    break
            if next == -1:
                return j
            fnexts.append(i)
        return fnexts.index(max(fnexts))
    return frame_num


def get_next_frame(algo, frame_table, addrs):
    frame_num = 0
    if algo == "FIFO":
        frame_num = FIFO()
    if algo == "LRU":
        frame_num = LRU(frame_table)
    if algo == "OPT":
        frame_num = OPT(frame_table, addrs)
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
    frame_num = get_next_frame(algo, frame_table, addrs)
    for i, entry in enumerate(page_table):
        if entry[0] == frame_num:
            page_table[i] = (frame_num, False)
            if (i, frame_num) in TLB:
                TLB.remove((i, frame_num))
    page_table[page_num] = (frame_num, True)
    frame_table[frame_num] = page_num
    updateTLB(TLB, page_num, frame_num)
    return page_table, TLB, frame_num, frame_table

if __name__ == '__main__':
    file, num_frames, algo = read_args()
    print("simulating %d frames from %s with %s" % (num_frames, file, algo))
    addrs = read_file(file)
    #for i, addr in enumerate(addrs):
    #    print("%d: %s" % (i, addr))
    TLB = []
    page_table = [(None, False)] * 256
    LRU_table = [None] * num_frames
    frame_table = [-1] * num_frames
    file = open("BACKING_STORE.bin", "rb")
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
                page_table, TLB, fnum, frame_table = table_update(page_table, TLB, algo, frame_table, page_num, addrs)
            else:
                LRU_table[fnum] = recency_value
                recency_value = recency_value + 1
        else:
            LRU_table[fnum] = recency_value
            recency_value = recency_value + 1


        file.seek(page_num * 256)
        frame = file.read(256) #whole frame
        file.seek(int(addr))
        byteref = file.read(1)
        print("%d, %s, %d,\n%s" % (int(addr), int.from_bytes(byteref, 'big'), fnum, frame.hex()))
        addr_index += 1
    #print hit and fault rates
    num_addrs = len(addrs)
    print("Number of Translated Addreses = %d" % num_addrs)
    print("Page Faults = %d\nPage Fault Rate = %.3f" % (page_faults, page_faults / num_addrs))
    print("TLB hits = %d\nTLB Misses = %d\nTLB Hit Rate = %.3f" % (num_addrs - tlbmiss, tlbmiss, tlbmiss / num_addrs))
    file.close()