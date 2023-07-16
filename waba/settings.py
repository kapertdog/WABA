"""
    This supposes to be universal settings API for all save-able data
"""
import json
import yaml
from pathlib import Path


class App:
    folder_path: Path = Path()
    mode: ...
    storages: ...
    ...


app = App()


class Folder:
    app: App = app
    ...


class MainFolder(Folder):
    ...


class PluginFolder(Folder):
    ...


class Group:
    folder: Folder
    ...


def setup(folder_name: str, place: str = "appdata"):  # place can be "appdata" | "localappdata" | "near"
    ...
