"""
just "about" with auto-generators for internal use
"""
from dataclasses import dataclass
from pathlib import Path
import argparse

"""
    HARD-WRITEN DATA
"""

shortname = "Waba"
fullname = "Windows Automatic Brightness Adjustment tool"
exe_name = "waba.exe"
description = "Automatic brightness adjustment tool"
legal_copyright = "(c) MIT License 2023 @kapertdog"
dev = "@kapertdog"
contact = "kapertdog@outlook.com"
company = "Strange Dog's Workshop"

version_path = Path("./info/version")
versionfile_path = Path("../packing/versionfile.txt")

"""
    GENERATORS
"""

greek_names = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon"
)


@dataclass
class Version:
    major: int = 0
    minor: int = 0
    patch: int = 0
    build: int = 0
    codename: str = ""

    def format(self, text: str, mode: str = "braces") -> str:
        match mode:
            case "pct":
                return text % self.__dict__
            case "braces":
                return text.format(**self.__dict__)
            case "both":
                return (text % self.__dict__).format(**self.__dict__)

    def write(self, filename: str = "version"):
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(self.__str__())

    def load(self, filename: str = "version"):
        with open(filename, "r+", encoding="utf-8") as file:
            data = file.read()
        if "+" in data:
            data, self.build = data.split("+")
        if "-" in data:
            data, self.codename = data.split("-")
        self.major, self.minor, self.patch = data.split(".")

    def semver(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self):
        return self.semver() + (
            f"-{self.codename}" if self.codename else "") + (
            f"+{self.build}" if self.build else "")


"""
    Preparing
"""

version = Version()

if version_path.exists():
    version.load()

"""
    CLI 
"""


def increase(name: str, value: str):

    print(f"Are you sure wanna increase {name} to {value}?")
    print("")
    if input("Y/N >> ").lower() in ("y", "yes"):
        ...
    else:
        ...
    ...

# info.py -i patch


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Centralizing app info in one place",

    )
    parser.add_argument()
    args = parser.parse_args()
    ...
