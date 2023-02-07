import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        options = ["Всегда", "Всегда",
                   "Только при автозагрузке", "Только при запуске пользователем",
                   "Никогда"]
        ...
        self.boot_sect = ttk.Labelframe(self, text="Загрузка", padding=10)
        self.boot_sect.pack()
        ...
        self.silent_boot_frame = ttk.Frame(self.boot_sect)
        self.silent_boot_frame.pack(anchor="w")

        self.silent_boot_lbl = ttk.Label(
            self.silent_boot_frame,
            text="Тихая загрузка")
        self.silent_boot_lbl.pack(side=LEFT)
        self.silent_boot_om = ttk.OptionMenu(
            self.silent_boot_frame,
            ttk.StringVar(),
            *options,
            bootstyle="outline",
        )
        self.silent_boot_om.pack(side=LEFT, padx=5, pady=5)
        ...
        self.fast_boot_frame = ttk.Frame(self.boot_sect)
        self.fast_boot_frame.pack(anchor="w")

        self.fast_boot_lbl = ttk.Label(
            self.fast_boot_frame,
            text="Быстрая загрузка"
        )
        self.fast_boot_lbl.pack(side=LEFT)

        self.fast_boot_om = ttk.OptionMenu(
            self.fast_boot_frame,
            ttk.StringVar(),
            *options,
            bootstyle="outline",
        )
        self.fast_boot_om.pack(side=LEFT, padx=5, pady=5)
    ...


if __name__ == "__main__":
    app = ttk.Window(title="title", themename="darkly")
    App(app)
    app.mainloop()
    ...
