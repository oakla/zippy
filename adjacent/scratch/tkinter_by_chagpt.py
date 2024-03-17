import tkinter as tk
from tkinter import messagebox, filedialog

# Function to display a message
def show_message():
    messagebox.showinfo("Message", "Please select a file.")

def close_dialogue():
    root.destroy()

# Function to ask for a file path
def ask_for_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("File Selected", f"You selected: {file_path}")

# Create the main window
root = tk.Tk()
root.title("Message and File Path")

# Create a label
label = tk.Label(root, text="Click the button to select a file:")
label.pack(padx=20, pady=20)

# Create a "Show Message" button
# message_button = tk.Button(root, text="Show Message", command=show_message)
message_button = tk.Button(root, text="Abort and close", command=close_dialogue)
message_button.pack()

# Create a "Select File" button
file_button = tk.Button(root, text="Select File", command=ask_for_file)
file_button.pack()

# Start the tkinter main loop
root.mainloop()
