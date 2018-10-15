from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import os
import re



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

@app.route("/label")
@app.route('/label/<start>')
def index(start=None):

    return render_template('label.html')

@app.route("/images")
def get_images(start=None):
    with open('labels.txt', 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR) 
        #print("Hello" + f.readline().decode())
        last = f.readline().decode()
    lastImg = last.split(",")[0]
    images = os.listdir(os.path.join(app.static_folder, "images"))
    #print(images)
    images.sort(key=alphanum_key)
    index = images.index(lastImg)
    images = images[index:len(images)]
    #print(images)
    return jsonify(images)

@app.route("/label", methods=['POST'])
def label_images():
    
    frame = request.get_json()['frame']
    label = request.get_json()['label']
    with open("labels.txt","a") as fo:
        fo.write(f"{frame},{label}\n")
    return label



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
