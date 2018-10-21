import os
import string


def get_last_line(fPath):
    if os.path.exists(fPath):
        with open(fPath, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR) 
            #print("Hello" + f.readline().decode())
            last = f.readline().decode()
            return last
    else:
        return None

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
dir_path = os.path.join(dir_path, "static", "images", "20161001_120007")
fPath = os.path.join(dir_path, "labels.txt")
rPath = os.path.join(dir_path, "results.txt")
last = get_last_line(fPath)
current_state  = "stop"
varr = last.split(",")
frame = varr[0]
frames = int(frame[5:frame.find(".")])
with open(fPath, 'rb') as f:
    with open(rPath, 'a') as fw:
        lblLine = f.readline().decode()
        varr = lblLine.split(",")
        frame = varr[0]
        lbl_count = int(frame[5:frame.find(".")])
        lbl_state = varr[1][:len(varr[1])-2]
        print("Looping through " + str(frames))        
        for index in range(frames):
            curr_frame = "frame" + str(index)
            if index < lbl_count:
                fw.write(f"{curr_frame},{current_state}\n")
            if index == lbl_count:
                print("Checking if state chage for " + str(lbl_count))
                print(curr_frame)
                current_state = lbl_state
                fw.write(f"{curr_frame},{current_state}\n")
                lblLine = f.readline().decode()
                varr = lblLine.split(",")
                frame = varr[0]
                lbl_count = int(frame[5:frame.find(".")])
                lbl_state = varr[1][:len(varr[1])-2]
                print(curr_frame)
            

            

#\static\images\20161001_120007