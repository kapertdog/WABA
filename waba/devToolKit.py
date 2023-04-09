import tkinter as tk
from tkinter import ttk
import sv_ttk

# import main
import info
import version_wrapp

tool_name = "DevToolKit"
title = f"{info.shortname}: {tool_name}"

"""
    Functions
"""

...

"""
    Interface
"""


def changePageGenerator(current: tk.Frame, target: tk.Frame):
    return lambda: current.master.changePage(target(current.master))


class Window(tk.Tk):
    page: tk.Frame = None

    def changePage(self, newPage: tk.Frame):
        if self.page:
            self.page.destroy()
        self.page = newPage
        self.page.pack(fill=tk.BOTH)


class VersionPicker(tk.Frame):

    def __init__(self, *args, oldVersion: info.Version = info.version, **kwargs):
        super().__init__(*args, **kwargs)
        self.major = ttk.Spinbox(self, from_=0, to=999)
        self.major.set(oldVersion.major)
        self.minor = ttk.Spinbox(self, from_=0, to=999)
        self.minor.set(oldVersion.minor)
        self.patch = ttk.Spinbox(self, from_=0, to=999)
        self.patch.set(oldVersion.patch)
        self.codename = ttk.Entry(self)
        self.codename.insert(0, oldVersion.codename)

        for i in range(2):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        grid_settings = {
            "ipadx": 4,
            "ipady": 4,
            "padx": 4,
            "pady": 4,
            "sticky": "NSEW"
        }

        tk.Label(self, text="Major").grid(row=0, column=0, **grid_settings)
        self.major.grid(row=1, column=0, **grid_settings)
        tk.Label(self, text="Minor").grid(row=0, column=1, **grid_settings)
        self.minor.grid(row=1, column=1, **grid_settings)
        tk.Label(self, text="Patch").grid(row=0, column=2, **grid_settings)
        self.patch.grid(row=1, column=2, **grid_settings)
        tk.Label(self, text="Codename").grid(row=0, column=3, **grid_settings)
        self.codename.grid(row=1, column=3, **grid_settings)

    def get(self):
        return info.Version(
            major=int(self.major.get()),
            minor=int(self.minor.get()),
            patch=int(self.patch.get()),
            codename=str(self.codename.get())
        )
    ...


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topFrame = tk.Frame(self)
        self.topFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.title = tk.StringVar(self, "")

        self.topLabel = tk.Label(self.topFrame, textvariable=self.title)
        self.topLabel.pack(anchor=tk.CENTER)
        self.setup()

    def setup(self) -> None:
        ...


class MainMenu(Page):
    def setup(self) -> None:
        self.title.set("This is Main")
        ttk.Button(
            self, command=changePageGenerator(self, VersionChanger),
            text="Update Version..."
        ).pack()
        ttk.Button(
            self, command=sv_ttk.toggle_theme,
            text="Toggle sv_ttk"
        ).pack()


class VersionChanger(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_row = tk.Frame(self)
        self.center_row.pack(fill=tk.Y, anchor=tk.CENTER)
        tk.Label(self.center_row, text="This is VersionChanger").pack(padx=10, pady=10)

        tk.Label(self.center_row, text="Current version:").pack()
        self.oldVersionText = tk.Label(self.center_row, font="Arial 20", text="---")
        self.oldVersionText.pack(pady=(0, 5))

        self.oldVersionText["text"] = str(info.version)

        self.versionPicker = VersionPicker(self.center_row)
        self.versionPicker.pack()

        ttk.Button(
            self, command=changePageGenerator(self, MainMenu),
            text="Back to Main"
        ).pack()

        self.bottomToolbar = tk.Frame(self.center_row)
        self.bottomToolbar.pack(side=tk.BOTTOM, fill=tk.X, ipadx=4, ipady=4)
        ttk.Button(
            self.bottomToolbar, command=self.apply,
            text="Apply"
        ).pack(side=tk.RIGHT, padx=4, pady=4)
        self.doClearBuilds = tk.BooleanVar(self.center_row, True)
        ttk.Checkbutton(
            self.bottomToolbar, text="Clear Builds amount",
            variable=self.doClearBuilds, offvalue=False, onvalue=True
        ).pack(side=tk.RIGHT, padx=4, pady=4)
        self.autoWrapping = tk.BooleanVar(self.center_row, True)
        ttk.Checkbutton(
            self.bottomToolbar, text="Wrap changes",
            variable=self.autoWrapping, offvalue=False, onvalue=True
        ).pack(side=tk.RIGHT, padx=4, pady=4)

    def apply(self):
        if self.doClearBuilds.get():
            info.version.build = 0
        info.version.read(str(self.versionPicker.get()))
        info.version.write()
        self.oldVersionText["text"] = str(info.version)
        if self.autoWrapping.get():
            version_wrapp.wrapp()


class Build(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    window = Window(screenName="VersionControlTool")
    window.geometry("800x400")
    window.title(title)
    window.changePage(MainMenu(window))
    window.mainloop()
