import tkinter as tk
import random

# Random name parts
prefixes = ["Gold", "Silver", "Green", "White", "Rose", "Berg", "Stone", "Levy", "Klein", "Adler", "Weiss"]
suffixes = ["man", "berg", "stein", "feld", "son", "baum", "witz", "er", "thal"]

def generate_last_name():
    return random.choice(prefixes) + random.choice(suffixes)

def on_click():
    # Generate a new name and update the label
    name = generate_last_name()
    label.config(text=name)

# Create the main window
root = tk.Tk()
root.title("Random Name Generator")
root.geometry("300x200")

# Label to display the name
label = tk.Label(root, text="Click the button!", font=("Helvetica", 16))
label.pack(pady=20)

# Button to generate names
button = tk.Button(root, text="Generate Name", command=on_click, font=("Helvetica", 14))
button.pack(pady=10)

# Start the app
root.mainloop()
