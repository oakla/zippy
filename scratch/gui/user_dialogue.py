import tkinter as tk
from tkinter import simpledialog
import random
import string

# Function to generate a random password
def generate_password():
    length = 12  # You can adjust the password length as needed
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Create the main application window
root = tk.Tk()
root.title("Password Chooser")

# Function to handle button click event
def choose_password():
    suggested_password = generate_password()
    user_password = simpledialog.askstring("Password Input", "Choose a password or use the suggested one:", initialvalue=suggested_password)
    if user_password is not None:
        # User entered a password
        print("User chose:", user_password)
    else:
        # User canceled the input dialog
        print("User canceled")

# Create a button to trigger the password dialog
password_button = tk.Button(root, text="Choose Password", command=choose_password)
password_button.pack(padx=20, pady=20)

# Start the main GUI loop
root.mainloop()
