import tkinter as tk
from tkinter import simpledialog

# Function to update the text input based on the selected radio button
def update_text_input():
    selected_option = radio_var.get()

    if selected_option == "Option 1":
        input_var.set("Option 1 selected")
    elif selected_option == "Option 2":
        input_var.set("Option 2 selected")
    elif selected_option == "Option 3":
        input_var.set("Option 3 selected")

# Create the main application window
root = tk.Tk()
root.title("Radio Button Dialog")

# Create a variable to store the selected radio button value
radio_var = tk.StringVar()

# Create radio buttons
radio_option1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value="Option 1", command=update_text_input)
radio_option2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value="Option 2", command=update_text_input)
radio_option3 = tk.Radiobutton(root, text="Option 3", variable=radio_var, value="Option 3", command=update_text_input)

radio_option1.pack()
radio_option2.pack()
radio_option3.pack()

# Create a text input box
input_var = tk.StringVar()
text_input = tk.Entry(root, textvariable=input_var)
text_input.pack()

# Function to open the dialogue
def open_dialogue():
    update_text_input()
    result = simpledialog.askstring("Radio Button Dialog", "Choose an option:", initialvalue=input_var.get())
    if result is not None:
        input_var.set(result)

# Create a button to trigger the dialogue
dialogue_button = tk.Button(root, text="Open Dialogue", command=open_dialogue)
dialogue_button.pack()

# Start the main GUI loop
root.mainloop()
