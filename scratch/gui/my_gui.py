
import tkinter as tk
from tkinter import simpledialog
import random
import string
import pyperclip


words = [
    'spirochetemia',
    'lithontriptic',
    'heptadecyl',
    'stepbrother',
    'mineowner',
    'copywriters',
    'MAXI',
    'astringes',
    'parathymic',
    'widowmen']


def keep_fooing(key:str):
    pyperclip.copy(key)
    print(key)

# Create a function to handle the button click event
def button_click(option, text_input):
    if option == 1:
        keep_fooing(text_input.get())
    elif option == 2:
        keep_fooing(text_input.get())
    elif option == 3:
        print("Selected Option", f"You entered: {text_input.get()}")
    else:
        print("No option selected")
    root.destroy()

# Function to update the text input based on the selected radio button
def update_text_input():
    selected_option = radio_var.get()

    if selected_option == 1:
        input_var.set(generate_passpharse())
    elif selected_option == 2:
        input_var.set(generate_password())
    elif selected_option == 3:
        input_var.set("")

def generate_passpharse(k_words:int=3):
    passpharse = []
    for i in range(k_words):
        passpharse.append(random.choice(words))
    return " ".join(passpharse)

def generate_password(length:int = 8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password



# Create the main application window
root = tk.Tk()
root.title("Radio Button Dialog")

# Create a variable to store the selected radio button value
radio_var = tk.IntVar()

# Create radio buttons
radio_option1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value=1, command=update_text_input)
radio_option2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value=2, command=update_text_input)
radio_option3 = tk.Radiobutton(root, text="Option 3", variable=radio_var, value=3, command=update_text_input)

radio_option1.pack()
radio_option2.pack()
radio_option3.pack()

# Create a text input box
input_var = tk.StringVar()
text_input = tk.Entry(root, textvariable=input_var)
text_input.pack()


# Create a button to trigger the dialogue
dialogue_button = tk.Button(root, text="Open Dialogue", command=lambda: button_click(radio_var.get(), text_input))
dialogue_button.pack()


# Start the main GUI loop
root.mainloop()

