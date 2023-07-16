"""
    just "about" with auto-generators for internal use but
    this supposes to be info-data storage standards and utilities
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

is_portable = Path("./info/.portable").exists()

greek_names = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon"
)

version_warning = "\n" "# Following semver.org" \
                  "\n" "# Yes it's reading version from there"


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

    def read(self, semver_text: str):
        if "+" in semver_text:
            semver_text, self.build = semver_text.split("+")
        if "-" in semver_text:
            semver_text, self.codename = semver_text.split("-")
        self.major, self.minor, self.patch = semver_text.split(".")
        return self

    def write(self, filename: str = version_path):
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(self.__str__() + version_warning)

    def load(self, filename: str = version_path):
        with open(filename, "r+", encoding="utf-8") as file:
            self.read(file.readline().rstrip("\n"))

    def semver(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def win_ver(self):
        return f"{self.semver()}.{self.build}"

    def __str__(self):
        return self.semver() + (
            f"-{self.codename}" if self.codename else "") + (
            f"+{self.build}" if self.build else "")

    def __setitem__(self, key: str, value: int | str):
        self.__dict__[key] = value

    def __copy__(self):
        return Version(*self.__dict__)


"""
    Preparing
"""
# NOTE: This module not suppose to execute anything, operations like
# version file loading need to be implemented only as callable from main class functions

version = Version()

if version_path.exists():
    version.load()

"""
    CLI 
"""


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,

    )
    args = parser.parse_args()
    ...
