import os
import random
import time
import tkinter as tk
from PIL import Image, ImageTk


#defines folders
folders ={
"Characters": r"C:\Users\Jan\Desktop\Program files\artref\Characters",
"Poses": r"C:\Users\Jan\Desktop\Program files\artref\Poses",
"Clothes": r"C:\Users\Jan\Desktop\Program files\artref\Clothes"
}
displayed_labels = {"Clothes": None, "Poses": None, "Characters": None}
displayed_images = []




def image(category):
    #removes hags

    if category == "All":
        for label in window.winfo_children():
            if isinstance(label, tk.Label):
                label.destroy()
        for name, path in folders.items():
            files = os.listdir(path)
            choice = random.choice(files)
            img = Image.open(path + "\\" + choice)
            img = img.resize((500, 700))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(window, image=photo)
            displayed_labels[name] = label
            label.pack(side="left",fill="y",)
            window.geometry("900x900")
            displayed_images.append(photo)
    else:
        if displayed_labels.get(category) is not None:
            displayed_labels[category].destroy()
            displayed_labels[category] = None
        path = folders[category]
        files = os.listdir(path)
        choice = random.choice(files)
        img = Image.open(path + "\\" + choice)
        img = img.resize((500, 700))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=photo)
        displayed_labels[category] = label
        label.pack(side="left", fill="y", )
        window.geometry("900x900")
        displayed_images.append(photo)
time.sleep(1)





#window
window = tk.Tk()
window.title("Artref")
button =tk.Button(window, text="All", width=20, command=lambda: image("All")).pack()
button =tk.Button(window, text="Clothes", width=20, command=lambda: image("Clothes")).pack()
button =tk.Button(window, text="Poses", width=20, command=lambda: image("Poses")).pack()
button =tk.Button(window, text="Characters", width=20, command=lambda: image("Characters")).pack()

tk.mainloop()





