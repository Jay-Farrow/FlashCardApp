import tkinter as tk
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv(".\data\words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data\\hiragana.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Hiragana", fill="black")
    canvas.itemconfig(card_word, text=current_card["hiragana"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)



def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="romaji", fill="white")
    canvas.itemconfig(card_word, text=current_card["romaji"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data\words_to_learn.csv", index=False)
    next_card()


#-------------- User Interface ------------------#
window = tk.Tk()
window.title("What are Flash Cards?")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip_card)

# Centering Window on the Screen and creating window size.
window_width = 1000
window_height = 800
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Creating canvas and objects
canvas = tk.Canvas(width=900, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = tk.PhotoImage(file=".\images\card_front.png")
card_back_img = tk.PhotoImage(file=".\images\card_back.png")
card_background = canvas.create_image(450, 270, image=card_front_img)
card_title = canvas.create_text(450, 200, text="French", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(450, 300, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# Creating buttons
cross_image = tk.PhotoImage(file=".\images\wrong.png")
cross_button = tk.Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(column=0, row=1)

check_image = tk.PhotoImage(file=".\images\\right.png")
check_button = tk.Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=1)

next_card()

window.mainloop()
