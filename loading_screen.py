"""
    Неиспользуемый кусок. Хотел сделать красиво, не получилось...
"""
import tkinter as tk


def load_screen():
    screen = tk.Tk()

    title_lbl = tk.Label(screen, text="WABA v.Dev_B\nmade by @kapertdog")
    loading_lbl = tk.Label(screen, font=100, text="LOADING")

    loading_lbl.grid()
    title_lbl.grid()

    screen.after(2000, screen.destroy)

    screen.mainloop()


def do_it_all(*args):
    def q():
        for i in args:
            i()
    return q


def processing(func, title="Waba: Processing", message="Processing..."):
    window = tk.Tk()
    window.title(title)
    text = tk.Label(window, text=message, font=200, pady=20, padx=20)
    text.grid()
    func = do_it_all(func, window.destroy)
    window.after(0, func)
    window.mainloop()
