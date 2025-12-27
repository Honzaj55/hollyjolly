import random
import tkinter as tk

hex_chars = "ABCDEF0123456789"

def generate_hex():
    code = ""
    for _ in range(6):
        code +=  random.choice(hex_chars)
    return "#" + code

# generate the first color
color = generate_hex()
print(color)


def validate_hex(P):
    if P== "":
        return True
    if len(P) > 6:
        return False
    for c in P.upper():
        if c not in "ABCDEF0123456789":
            return False
    return True

def Check_guess():
    user_guess = guess.get()
    r = int(color[1:3],16)
    g = int(color[3:5],16)
    b = int(color[5:7],16)
    max_distance = (255**2 + 255**2 + 255**2)**0.5
    guess_r = int(user_guess[1:3],16)
    guess_g = int(user_guess[3:5],16)
    guess_b = int(user_guess[5:7],16)
    #distance = ((r - guess_r)**2 + (g - guess_g)**2 + (b - guess_b)**2)**0.5 actual rgb
    distance = ((2*(r - guess_r)**2 + 4*(g - guess_g)**2 + 3*(b - guess_b)**2)**0.5) / 3 #human eye
    similarity = max(0, 100 - (distance / max_distance) * 100)
    result.config(text=f"Similarity: {similarity:.2f}%")
    user_guess = guess.get().upper()
    guess_color.config(bg="#" + user_guess)
    correct_color.config(text=f"Correct Color: {color}")
    
def new_color():
    global color
    color = generate_hex()
    window.configure(bg=color)
    guess.delete(0, tk.END)
    result.config(text="")
    correct_color.config(text="")





window= tk.Tk()
window.title("Color Generator")
window.geometry("400x400")
window.configure(bg=color)


vcmd = window.register(validate_hex)
guess = tk.Entry(window, validate="key", validatecommand=(vcmd, "%P"))
guess.pack(pady=20)

submit = tk.Button(window, text="Submit", command=Check_guess)
submit.pack(pady=10)

result = tk.Label(window, text="")
result.pack(pady=10)

guess_color = tk.Frame(window, width=100, height=100, bg="#FFFFFF")
guess_color.pack(pady=10)

correct_color = tk.Label(window, text="") 
correct_color.pack(pady=10)

generate = tk.Button(window, text="Generate New Color", command=new_color)
generate.pack(pady=10)



window.mainloop()
