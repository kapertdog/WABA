# -*- coding: utf-8 -*-
from pathlib import Path


def autostart(switch: bool = True, edition: str = "exe"):
    match switch:
        case True:
            from winshell import CreateShortcut, programs
            startup_program_files = Path(programs(), "Startup",  "Waba.lnk")
            if edition in ("exe", "folder"):
                target = "./WABA v.Dev_B.exe"
            elif edition == "venv":
                target = "./start_vB.cmd"
            else:
                raise ValueError(edition)
            CreateShortcut(
                Path=str(startup_program_files),
                StartIn=str(Path.cwd()),
                Target=target
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
