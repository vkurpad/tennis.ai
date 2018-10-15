import cv2
vidcap = cv2.VideoCapture('1a.mov')
success,image = vidcap.read()
count = 0
i = 0
fps = vidcap.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

while success:
    if (i % (fps * 2) == 0): # Sampled 1 frame every 2 seconds
        
        cv2.imwrite("frame%d.jpg" % i, image)     # save frame as JPEG file  
        count += 1    
    success,image = vidcap.read()
    
    
    i+=1
print('Processed : %d frames. Output is %d frames' % (i, count))