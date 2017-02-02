from os import listdir
from os.path import isfile, join, isdir
import random
import Tkinter as tk
from PIL import Image
from PIL import ImageTk

PATH = "./session-1"

experiment_sequence = []

samples_sets = [f for f in listdir(PATH) if isdir(join(PATH,f))]

print "Generating experiment_sequence"

for samples_set in samples_sets:
    set_files = [f for f in listdir(PATH+"/"+samples_set) if f.endswith(".bmp")]
    
    if "original.bmp" in set_files:
        set_files.remove("original.bmp")
    else:
        print "Warning: no original file. Skipping this set"
        continue

    for item in set_files:
        l = [PATH+"/"+samples_set+"/original.bmp", PATH+"/"+samples_set+"/"+item]
        random.shuffle(l)
        experiment_sequence.append(l)

random.shuffle(experiment_sequence)

print experiment_sequence

print "Starting session..."

#root = tk.Tk()
#root.title("ACR Testbench - "+PATH)
#root.geometry('1025x1025')
#cv = tk.Canvas(root, width=1024, height=1024)
#cv.pack()

#root.mainloop()

# for each test pair
for pair in experiment_sequence:
    mediaA = pair[0];
    mediaB = pair[1];

    im = Image.open(mediaA)
    #im = im.resize((1024,1024), Image.ANTIALIAS)
    im.show()
    #image = ImageTk.PhotoImage(im)
    #imagesprite = cv.create_image(511,511,image=image)
    

    # pic = tk.PhotoImage(file=mediaA)
    input("Enter any key: ")
    im = Image.open(mediaB)
    im.show()
    input("Enter any key: ")

print "End session..."
