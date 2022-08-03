# -*- coding: utf-8 -*-
from pathlib import Path
from winshell import CreateShortcut, programs
from os import remove, getenv


def autostart(switch: bool = True):
    match switch:
        case True:

            startup_program_files = Path(programs(), "Startup",  "Waba.lnk")
            CreateShortcut(
                Path=str(startup_program_files),
                Target="./WABA v.Dev_B.exe"
            )
            return True
        case False:
            remove(
                Path(
                    getenv("APPDATA"),
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs",
                    "Startup",
                    "Waba.lnk"
                    )
            )
            return False
