from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import os
import re

fileName = lambda x: x.split(".")[0]
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

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


app = Flask(__name__)
print("Hello")
@app.route("/")
def index(start=None):
    result = []
    videos = os.listdir(os.path.join(app.static_folder, "videos"))
    videoNames = map(fileName, videos)
    
    for vid in videoNames:
        if os.path.exists(os.path.join(app.static_folder, "images", vid)):
            # Check to see if the folder was processed completely. Last Frame in the labels.txt file
            lblPath = os.path.join(app.static_folder, "images", vid, "labels.txt")
            if os.path.exists(lblPath):
                last = get_last_line(lblPath)
                print(last)
                images = os.listdir(os.path.join(app.static_folder, "images", vid))
                #print(images)
                images.sort(key=alphanum_key)
                if(images[len(images) -1] != last):
                    result.append(vid)
                
            else:
                result.append(vid)

        else:        
            result.append(vid)
    return render_template('index.html', videos=result)

@app.route("/label")
@app.route('/label/<video>')
def label(video=None):
    return render_template('label.html', video=video)

@app.route("/images/<video>")
def get_images(video):
    fpath = os.path.join(app.static_folder, "images", video, "labels.txt")
    print("Getting images for " + video + " from " + fpath )
    last = get_last_line(fpath)
    images = os.listdir(os.path.join(app.static_folder, "images", video))
    images.sort(key=alphanum_key)
    print("Length = " + str(len(images)))
    if last != None:
        print("@@@@@@@@@@@@@@@@@@ Last is not none")
        print(last)
        lastImg = last.split(",")[0]
        index = images.index(lastImg)
        images = images[index:len(images)]
    #print(images)
    print("Length After = " + str(len(images)))
    
    #print(images)
    return jsonify(images)

@app.route("/label/<video>", methods=['POST'])
def label_images(video):
    fpath = os.path.join(app.static_folder, "images", video, "labels.txt")
    frame = request.get_json()['frame']
    label = request.get_json()['label']
    with open(fpath,"a") as fo:
        fo.write(f"{frame},{label}\n")
    return label



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
