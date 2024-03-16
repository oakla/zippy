import tkinter as tk
from tkinter import messagebox

win = tk.Tk()

message_box = tk.Toplevel(win)

def show_common_password_warning(self):
    answer = messagebox.askyesno(
        master=self.root,
        text="Password Warning",
        message="Are you sure you want to conintue?",
        details="Your password is included in a list of the 100,000 most commonly used passwords, and therefore is easily crackable.",
        icon=messagebox.WARNING,
    )
    if answer == False:
        return 

win.geometry("450x400")
# new_win = tk.Toplevel(win)
# new_win.geometry("700x250")
# new_win.title("NEW WINDOW")
# new_win.withdraw()
# tk.Label(new_win, text="Example Label", font=('Helvetica 15 bold')).pack(pady=10)


def show_new():
    new_win.grab_set()
    new_win.deiconify()


def show_old():
    new_win.grab_release()
    new_win.withdraw()


def print_text():
    print("BUTTON IS PRESSED")


button = tk.Button(win, text="Show",command= show_new)
button.pack(pady=50)
button_text = tk.Button(win, text="print",command=print_text)
button_text.pack(pady=100)

button2 = tk.Button(new_win, text="OK",command= show_old)
button2.pack(pady=50)

win.mainloop()