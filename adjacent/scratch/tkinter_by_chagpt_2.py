import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk

def show_message():
    messagebox.showinfo("Message", "Please select a file.")

def ask_for_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("File Selected", f"You selected: {file_path}")

root = tk.Tk()
root.title("Message and File Path")

# Set the theme
style = ttk.Style()
style.theme_use("clam")

label = tk.Label(root, text="Click the button to select a file:", font=("Arial", 12))
label.pack(padx=20, pady=10)

message_button = tk.Button(root, text="Show Message", command=show_message, bg="lightblue", fg="black", font=("Arial", 12))
message_button.pack(pady=10)

file_button = tk.Button(root, text="Select File", command=ask_for_file, bg="lightgreen", fg="black", font=("Arial", 12))
file_button.pack(pady=10)

root.mainloop()
