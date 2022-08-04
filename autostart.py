# -*- coding: utf-8 -*-
from pathlib import Path


def autostart(switch: bool = True):
    match switch:
        case True:
            from winshell import CreateShortcut, programs
            startup_program_files = Path(programs(), "Startup",  "Waba.lnk")
            CreateShortcut(
                Path=str(startup_program_files),
                Target="./WABA v.Dev_B.exe"
            )
            return True
        case False:
            from os import remove, getenv
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
