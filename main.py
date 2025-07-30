import os.path
from tkinter import *
import pandas
import random

LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
BACKGROUND_COLOR = "#B1DDC6"
english_match = ""

window = Tk()
window.config(background=BACKGROUND_COLOR, padx=50, pady=50, highlightthickness=0)

# FRONT CARD
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
main_image = PhotoImage(file="images/card_front.png")
new_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, anchor="center", image=main_image)
language_text = canvas.create_text(400, 153, anchor="center", text="Language", font=LANGUAGE_FONT)
word_text = canvas.create_text(400, 263, anchor="center", text="Word", font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

# Opening CSV with pandas

try:
    learn_data = pandas.read_csv("data/words_to_learn.csv")
    new_spanish_data = learn_data.to_dict(orient="records")
except FileNotFoundError:
    spanish_data = pandas.read_csv("data/spanish_words.csv")
    new_spanish_data = spanish_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    # if os.path.exists("data/words_to_learn.csv"):
    #     os.remove("data/words_to_learn.csv")
    spanish_data = pandas.read_csv("data/spanish_words.csv")
    new_spanish_data = spanish_data.to_dict(orient="records")


unknown_words_data = [item for item in new_spanish_data]


# print(new_spanish_data)

# 3 Seconds countdown and BACK CARD


def create_back_card():
    # global canvas_image
    # global language_text
    # global word_text
    # global new_image
    #
    # canvas.delete(language_text)
    # canvas.delete(word_text)
    # language_text = canvas.create_text(400, 153, anchor="center", text="English", font=LANGUAGE_FONT, fill="white")
    canvas.itemconfig(language_text, text="English", font=LANGUAGE_FONT, fill="white")
    # word_text = canvas.create_text(400, 263, anchor="center", text=f"{english_match}", font=WORD_FONT, fill="white")
    canvas.itemconfig(word_text, text=f"{english_match}", font=WORD_FONT, fill="white")
    canvas.itemconfig(canvas_image, image=new_image)


def cut_known_words():
    global unknown_words_data
    global english_match

    unknown_words_data = [d for d in unknown_words_data if d.get("English") != english_match]
    print(unknown_words_data)
    df = pandas.DataFrame(unknown_words_data)
    df.to_csv("data/words_to_learn.csv", index=False)


# def countdown(seconds):
#     global timer
#
#     if seconds > 0:
#         timer = window.after(1000, countdown, seconds - 1)
#     else:
#         create_back_card()


# Getting a random word from the dictionary


def random_spanish_word():
    # global word_text
    # global language_text
    global new_spanish_data
    global english_match
    # global canvas_image
    # global main_image
    global timer

    window.after_cancel(timer)
    spanish_list = [item["Spanish"] for item in new_spanish_data]
    random_word = random.choice(spanish_list)
    english_match = [item["English"] for item in new_spanish_data if item["Spanish"] == random_word]
    english_match = english_match[0]

    # canvas.delete(word_text)
    # canvas.delete(language_text)
    # language_text = canvas.create_text(400, 153, anchor="center", text="Spanish", font=LANGUAGE_FONT)
    canvas.itemconfig(language_text, anchor="center", text="Spanish", font=LANGUAGE_FONT, fill="black")
    # word_text = canvas.create_text(400, 263, anchor="center", text=f"{random_word}", font=WORD_FONT)
    canvas.itemconfig(word_text, anchor="center", text=f"{random_word}", font=WORD_FONT, fill="black")
    canvas.itemconfig(canvas_image, image=main_image)
    timer = window.after(3000, func=create_back_card)


# BUTTONS
timer = window.after(3000, func=create_back_card)

right_button = Button()
right_image = PhotoImage(file="images/right.png")
right_button.config(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=lambda: [random_spanish_word()
    , cut_known_words()])
right_button.grid(column=0, row=1)

wrong_button = Button()
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button.config(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=random_spanish_word)
wrong_button.grid(column=1, row=1)


window.mainloop()
