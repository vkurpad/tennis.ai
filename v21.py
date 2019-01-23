import cv2
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
f = "1b.mov"
f1 = f.split(".")[0]
fpath = os.path.join(dir_path, "static", "videos", f)
print(fpath)
vidcap = cv2.VideoCapture(fpath)
success,image = vidcap.read()
count = 0
i = 0
fps = vidcap.get(cv2.CAP_PROP_FPS)
fps = int(fps)
dimensions = image.shape
print('Image Dimension    : ',dimensions) 
info = os.path.join(dir_path, "static", "images", f1,"info.txt")

print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
imgPath = os.path.join(dir_path, "static", "images", f1)
#os.mkdir(imgPath)
with open(info, 'a') as fw:
    fw.write(f"{fpath}, {dimensions}, {fps}fps\n")
while success:
    if (i % 12 == 0): # Sampled 5 frames every second
        
        cv2.imwrite(os.path.join(imgPath, "frame%d.jpg" % i), image)     # save frame as JPEG file  
        count += 1    
    success,image = vidcap.read()
    
    if i == 7200:
        break
    i+=1
print('Processed : %d frames. Output is %d frames' % (i, count))