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


def processing(func, title="Waba: Processing", message="Processing...", fg: str = "black", bg: str = "white"):
    p_window = tk.Tk()
    p_window.title(title)
    text = tk.Label(p_window, text=message, font=200, pady=20, padx=20, bg=bg, fg=fg)
    text.grid()
    p_window.resizable(width=False, height=False)
    p_window.overrideredirect(True)
    # window.geometry(f"+{window.winfo_screenwidth() // 2}+{window.winfo_screenheight() // 2}")
    p_window.geometry(f"+{100}+{100}")
    do_it_func = do_it_all(func, lambda: p_window.quit)
    p_window.after(100, do_it_func)
    p_window.mainloop()
    p_window.destroy()
    print("-- ls quit")
