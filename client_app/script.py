from keras.models import load_model
from PIL import Image, ImageOps, ImageTk
import numpy as np
import tkinter as tk
from tkinter import BOTTOM, HORIZONTAL, Frame, Label, filedialog, ttk
import sys


# Load the model and set variables
model = load_model('dogs_model.h5')
size = (224, 224)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
breeds = ["Chihuahua", "Japanese spaniel", "Maltese", "Pekinese", "Shin Tzu", "Ibizan Hound", "Irish Terrier", "Boston Bull", "Golden Retriever", "Gordon Setter", "Rottweiler", "Tibetan Mastiff", "Samoyed", "Greater Swiss Mountain dog","Basset"]

flagNewFile = 1

def openFile():
    global imgtk
    global img
    global flagNewFile
    flagNewFile = 0
    lbl.grid_forget()
    name = filedialog.askopenfilename(initialdir="/",title="Select File", filetypes=(("JPG File","*.jpg"),("PNG File","*.png")))
    img = Image.open(name)
    imgtk = ImageTk.PhotoImage(img)
    lbl.configure(image=imgtk)
    textBreed.configure(text="Breed")
    textResults.configure(text="Certainty")
    progressBar['value'] = 0

def predict():
    global flagNewFile
    global img
    global breeds
    global index

    max = 0.0 
    index = -1

    if flagNewFile == 0:
        flagNewFile = 1
        image = ImageOps.fit(img, size, Image.ANTIALIAS)
        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        #Load the image into the array
        data[0] = normalized_image_array
        #predict
        prediction = model.predict(data)

        #find max and write results
        result_array = prediction[0]
        for i in range(len(result_array)):
            if result_array[i] > max:
                index = i
                max = result_array[i]

        #write results
        textBreed.configure(text="Breed: " + breeds[index])
        textResults.configure(text="Certainty: " + str(max*100) + "%") 
        progressBar['value'] = max*100


#gui
root = tk.Tk()
root.geometry("500x500")
root.title("Dogs Recognition")
root.iconbitmap("icon.ico")

frame = Frame(root)
frame.pack(side=BOTTOM, padx=15, pady=15)

placeholder = Image.open("placeholder.png")
placeholdertk = ImageTk.PhotoImage(placeholder)

lbl = Label(root)
lbl.configure(image=placeholdertk, padx = 10,pady=20)
lbl.pack()

textBreed = Label(frame,font = ("Times New Roman",16), text="Breed")
textBreed.pack()
textBreed['fg'] = "#263d42"

textResults = Label(frame,font = ("Times New Roman",16), text="Certainty")
textResults.pack()
textResults['fg'] = "#263d42"

progressBar = ttk.Progressbar(frame,orient=HORIZONTAL,length=300,mode='determinate')
progressBar.pack(pady=20)
progressBar['value'] = 0

btnOpenFileBtn = tk.Button(frame,text="Select Image", padx = 10,pady=5, fg="white",bg="#263d42", command=openFile)
btnOpenFileBtn.pack(side=tk.LEFT, padx=12)

btnExit = tk.Button(frame, text = "Exit", padx = 10,pady=5, fg="white",bg="#263d42", command = sys.exit)
btnExit.pack(side=tk.LEFT, padx=12) 

btnOpenCam = tk.Button(frame,text="Predict", padx = 10,pady=5, fg="white",bg="#263d42", command=predict)
btnOpenCam.pack(side=tk.LEFT, padx=12)

root.mainloop()